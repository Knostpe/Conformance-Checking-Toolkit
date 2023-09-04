import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pm4py
from PIL import Image
from pm4py.visualization.petri_net import visualizer as vis
from pm4py.visualization.petri_net.variants import token_decoration_frequency as tdf
from pm4py.visualization.petri_net.variants import token_decoration_performance as tdp
import base64

def get_log(uploaded_log, sep, timestamp_format = None):
    if uploaded_log[-3:] == 'xes':
        log = pm4py.read_xes(uploaded_log)
        log_csv = pm4py.convert_to_dataframe(log)

    elif uploaded_log[-3:] == 'csv':
        log_csv = pm4py.format_dataframe(pd.read_csv(uploaded_log, sep=sep), case_id='case:concept:name',
                                         activity_key='concept:name', timestamp_key='time:timestamp')
    else:
        st.error('You need to upload either a csv or xes file as event log', icon="🚨")

    log_csv = csv_prep(log_csv)
    log = pm4py.convert_to_event_log(log_csv)

    log_csv_show = log_csv.rename(
        columns={'case:concept:name': 'CaseID', 'concept:name': 'Event Type', 'time:timestamp': 'Timestamp',
                 'event_count': 'EventID'})

    if timestamp_format is not None:
        log_csv_show['Timestamp'] = log_csv_show['Timestamp'].dt.strftime(timestamp_format)

    return log, log_csv, log_csv_show

def get_model(uploaded_model):

    if isinstance(uploaded_model, str):
        model_filename = uploaded_model  # If 'demo' mode, 'uploaded_model' is already a string.
    else:
        model_filename = uploaded_model.name  # If 'file_uploader' mode, get the filename.

    pn, im, fm = pm4py.read_pnml('data/models/' + model_filename)



    return  pn, im, fm

def model_viz(pn, im, fm):
    pn_viz = pm4py.visualization.petri_net.common.visualize.apply(pn, im, fm)

    pn_viz.attr(rankdir='TB')  # Set the layout direction (Left to Right)
    pn_viz.attr(size=f"4,3!")
    pn_viz.attr(ratio="fill")  # This might help maintain aspect ratio
    st.graphviz_chart(pn_decorated_align)

    # pn_viz.attr(dpi="1500")
    # pn_viz.render('data/images/petri_net', format="png", cleanup=True)

def csv_prep(log_csv):
    log_csv = renumerate_case_ids(log_csv)
    log_csv['time:timestamp'] = pd.to_datetime(log_csv['time:timestamp'], format='mixed')
    log_csv = log_csv.sort_values(by='time:timestamp', ascending=True)
    log_csv['event_count'] = log_csv.groupby('case:concept:name').cumcount() + 1
    log_csv['case:concept:name'] = log_csv['case:concept:name'].astype(np.int64)
    log_csv = log_csv.sort_values(by=['case:concept:name', 'event_count'], ascending=True)
    log_csv['case:concept:name'] = log_csv['case:concept:name'].astype(str)
    log_csv = log_csv[['case:concept:name', 'concept:name', 'time:timestamp', 'event_count']]
    return log_csv


def renumerate_case_ids(data_frame, case_id_column='case:concept:name'):
    # Get the distinct case IDs
    distinct_case_ids = data_frame[case_id_column].unique()

    # Create a mapping dictionary to renumerate the case IDs
    case_id_mapping = {case_id: str(i + 1) for i, case_id in enumerate(distinct_case_ids)}

    # Replace the case IDs in the DataFrame with the renumerate values
    data_frame[case_id_column] = data_frame[case_id_column].map(case_id_mapping)

    return data_frame

def fitness_calc(log, pn, im, fm):
    fitness = pm4py.fitness_token_based_replay(log, pn, im, fm)
    return fitness

def fitness_compare_calc(log, pn, im, fm):

    alignment_result = pm4py.conformance_diagnostics_alignments(log, pn, im, fm)

    alignment_fitness = {}
    for i, trace in enumerate(alignment_result):
        fitness_value = trace['fitness']
        case_id = f'Case {i + 1}'
        alignment_fitness[case_id] = fitness_value

    fitness_df = pd.DataFrame.from_dict(alignment_fitness, orient='index', columns=['Alignment Fitness'])

    return fitness_df

def alignment_viz(log, pn, im, fm):
    pn_decorated_align = vis.apply(pn, im, fm, log, variant=vis.ALIGNMENTS)

    # Adjust layout engine and graph attributes
    pn_decorated_align.attr(rankdir='TB')  # Set the layout direction (Left to Right)
    pn_decorated_align.attr(size=f"4,3!")
    pn_decorated_align.attr(ratio="fill")  # This might help maintain aspect ratio
    st.graphviz_chart(pn_decorated_align)

    #pn_decorated_align.attr(dpi="1000")
    #pn_decorated_align.render('data/images/alignment_viz', format="png", cleanup=True)

def frequency_viz(log, pn, im, fm):
    pn_decorated_freq = tdf.apply(pn, im, fm, log)
    st.graphviz_chart(pn_decorated_freq)

def performance_viz(log, pn, im, fm):
    pn_decorated_perf = tdp.apply(pn, im, fm, log)
    st.graphviz_chart(pn_decorated_perf)

def fitness_viz(log_csv, log, pn, im, fm):

    fitness = fitness_calc(log, pn, im, fm)

    col1, col2, col3, col4 = st.columns(4)

    labels = ["Conformant Events", "Deviating Events", "Missing Events"]
    values = [len(log_csv[(~log_csv['missing']) & (~log_csv['is_deviation'])]),
              len(log_csv[log_csv['is_deviation']]),
              len(log_csv[log_csv['missing']])]

    col1.metric("Log Fitness", round(fitness['log_fitness'], 2), "")
    col1.metric(labels[0], values[0], "")

    col2.metric("Avg Trace Fitness", round(fitness['average_trace_fitness'], 2), "")
    col2.metric(labels[1], values[1], "")

    col3.metric("% of Fitting Traces", round(fitness['percentage_of_fitting_traces'], 2), "")
    col3.metric(labels[2], values[2], "")

    with col4:
        #Create a pie chart using Plotly Express
        st.write("")
        fig = go.Figure(data=[go.Pie(values=values,labels=labels, hoverinfo='label+percent', hole=0.5)])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.write("")

def render_svg(svg, width=None, height=None, zoom=None, open_in_new_tab=False):
    """Renders the given SVG string with optional size, zoom, and open in new tab customization."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')

    style = ""
    if width:
        style += f"width: {width};"
    if height:
        style += f"height: {height};"
    if zoom:
        style += f"zoom: {zoom};"


    html = f'<img src="data:image/svg+xml;base64,{b64}" style="{style}" />'

    st.write(html, unsafe_allow_html=True)

def read_svg_file(file_path):
    """Reads the SVG file and returns the SVG string."""
    with open(file_path, 'r') as file:
        svg_string = file.read()
    return svg_string

def plot_compare_calc(df):
    # Get the column name from the dataframe
    column_name = df.columns[0]

    # Calculate median and average fitness values
    median_fitness = df[column_name].median()
    average_fitness = df[column_name].mean()

    # Define custom colors for markers and lines
    marker_color = 'blue'
    line_color = 'red'

    # Create the scatter trace for data points
    scatter_trace = go.Scatter(
        x=df.index,
        y=df[column_name],
        mode='markers',
        marker=dict(color=marker_color),
        name='Fitness Data',
        text=df[column_name],  # Hover text for data points (fitness values)
    )

    # Create the line traces for median and average fitness
    median_trace = go.Scatter(
        x=[df.index[0], df.index[-1]],
        y=[median_fitness, median_fitness],
        mode='lines',
        line=dict(color=line_color, dash='dash'),
        name='Median Fitness',
        hoverinfo='text',  # Show hover info for the line
        hovertext=[f"Median Fitness: {median_fitness:.2f}"] * 2,  # Custom hover text for the line
    )

    average_trace = go.Scatter(
        x=[df.index[0], df.index[-1]],
        y=[average_fitness, average_fitness],
        mode='lines',
        line=dict(color=line_color),
        name='Average Fitness',
        hoverinfo='text',  # Show hover info for the line
        hovertext=[f"Average Fitness: {average_fitness:.2f}"] * 2,  # Custom hover text for the line
    )

    # Create the layout
    layout = go.Layout(
        title='Conformance Checking Results - Fitness Value per Case',
        xaxis=dict(title='Case ID'),
        yaxis=dict(title=column_name),
        hovermode='closest',
        plot_bgcolor='white',
    )

    # Create the figure and add the traces
    fig = go.Figure(data=[scatter_trace, median_trace, average_trace], layout=layout)

    # Update marker style for data points
    fig.update_traces(marker=dict(size=10, symbol='circle', line=dict(width=1, color=marker_color)))

    # Update axis style
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')

    # Update title style
    fig.update_layout(title_font=dict(size=16, family='Arial', color='black')) #IBM Plex Sans

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)

def plot_distribution(log_csv, distribution, type, aggregation, selected):

    if distribution == "Time" and aggregation == "Variants":
        st.warning("Oops! It looks like you've selected an invalid combination. "
                   "Variants can't be shown on a temporal scale. "
                   "Please choose a different combination.")
        return

    if distribution == 'Time':
        x_axis_label = 'Timestamp'
        x_tickformat = '%Y-%m-%d'  # Display year-month-day format
    elif distribution == 'Event ID':
        # Count the number of events per case and create a new DataFrame
        log_csv['event_count'] = log_csv.groupby('case:concept:name').cumcount() + 1
        x_axis_label = 'Event ID'
        x_tickformat = None

    if aggregation == "Variants":
        log_csv = create_variant_log_dict(log_csv)

    # Create a color map for event types (only if color_by_event_type is True)
    color_map = None
    if type == "Event Type":
        event_types = log_csv['concept:name'].unique()
        color_palette = ['blue', 'green', 'red', 'orange', 'purple', 'pink', 'brown', 'gray', 'olive', 'cyan']
        color_map = dict(zip(event_types, color_palette))

    # Create separate traces for deviations and conformant events (only if show_deviations is True)
    scatter_traces = []

    if type == "Deviation Type":

        conformant_events = log_csv[(~log_csv['missing']) & (~log_csv['is_deviation'])]
        deviation_events = log_csv[log_csv['is_deviation']]

        if aggregation == "Cases":
            hovertemplate = '<b>Date:</b> %{customdata|%Y-%m-%d}<br>' + '<b>Time:</b> %{customdata|%H:%M:%S}<br>' + '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Conformant'
        else:
            hovertemplate = '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Conformant'

        color = 'rgb(134, 228, 134)'  # Adjust the RGB values as needed

        conformant_trace = go.Scatter(
            x=(conformant_events['time:timestamp'] if distribution == "Time" else conformant_events['event_count']),
            y=conformant_events['case:concept:name'].astype(str),
            mode='markers',
            marker=dict(color=color, size=10, symbol='circle'),
            name='Conformant Events',
            text=conformant_events['concept:name'],  # Hover text for conformant event points
            customdata=conformant_events['time:timestamp'],
            hovertemplate=hovertemplate,
            legendgroup='Conformant Events',
        )
        scatter_traces.append(conformant_trace)

        if aggregation == "Cases":
            hovertemplate = '<b>Date:</b> %{customdata|%Y-%m-%d}<br>' + '<b>Time:</b> %{customdata|%H:%M:%S}<br>' + '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Deviating'
        else:
            hovertemplate = '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Deviating'

        color = 'rgb(220, 120, 0)'  # Adjust the RGB values as needed

        deviation_trace = go.Scatter(
            x=(deviation_events['time:timestamp'] if distribution == "Time" else deviation_events['event_count']),
            y= deviation_events['case:concept:name'].astype(str),
            mode='markers',
            marker=dict(color=color, size=10, symbol='x'),
            name='Deviating Events',
            text=deviation_events['concept:name'],  # Hover text for deviation points
            customdata=deviation_events['time:timestamp'],
            hovertemplate=hovertemplate,
            legendgroup='Deviating Events',
        )
        scatter_traces.append(deviation_trace)

        if aggregation == "Cases":
            hovertemplate = '<b>Date:</b> None<br>' + '<b>Time:</b> None<br>' + '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Missing'
        else:
            hovertemplate = '<b>Event:</b> %{text}<br>' + '<b>Result:</b> Missing'

        if distribution == 'Event ID':
            missing_events = log_csv[log_csv['missing']]
            missing_trace = go.Scatter(
                x=(missing_events['time:timestamp'] if distribution == "Time" else missing_events['event_count']),
                y= missing_events['case:concept:name'].astype(str),
                mode='markers',
                marker=dict(color='violet', size=10, symbol='square'),
                name='Missing Events',
                text=missing_events['concept:name'],  # Hover text for deviation points
                hovertemplate=hovertemplate,
                legendgroup='Missing Events',
            )
            scatter_traces.append(missing_trace)

    # Create separate traces for each event type (only if color_by_event_type is True)
    if type =="Event Type":
        if aggregation == "Cases":
            hovertemplate = '<b>Date:</b> %{customdata[0]|%Y-%m-%d} <br>' + '<b>Time:</b> %{customdata[0]|%H:%M:%S}<br>' + '<b>Event Type:</b> %{text}<br>' + '<b>Conformant:</b> %{customdata[1]}'
        else:
            hovertemplate = '<b>Event Type:</b> %{text}<br>' + '<b>Conformant:</b> %{customdata[1]}'

        for event_type in event_types:
            color = color_map[event_type]
            log_event_type = log_csv[log_csv['concept:name'] == event_type]
            trace = go.Scatter(
                x=(log_event_type['time:timestamp'] if distribution == "Time" else log_event_type['event_count']),
                y=log_csv[log_csv['concept:name'] == event_type]['case:concept:name'].astype(str),
                mode='markers',
                marker=dict(color=color, size=10),
                name=event_type,
                text=log_csv[log_csv['concept:name'] == event_type]['concept:name'],  # Hover text for data points (event_type values)
                hovertemplate= hovertemplate,
                customdata=np.stack((log_event_type['time:timestamp'], ['No' if is_deviation else 'Yes' for is_deviation in log_event_type['is_deviation']]), axis=-1),
                legendgroup=event_type,
            )
            scatter_traces.append(trace)

    # Create the layout
    layout, height = create_custom_layout(log_csv, distribution, x_axis_label, x_tickformat, aggregation, selected)

    # Create the figure and add the traces
    fig = go.Figure(data=scatter_traces, layout=layout)

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig, use_container_width=True, height=height)

def create_variant_log_dict(log_csv):

    case_dict = {}

    # Iterate through the DataFrame and populate the dictionary
    for category, values in log_csv.groupby('case:concept:name'):
        case_dict[category] = values.to_dict('records')

    flattened_data = {}

    for case, events in case_dict.items():
        flattened_events = [
            (
                event["concept:name"],
                "missing" if event["missing"] else "deviating" if event["is_deviation"] else "conformant",
            )
            for event in events
        ]
        flattened_data[case] = flattened_events

    unique_traces = {}
    selected_trace_ids = []

    for trace_id, events in flattened_data.items():
        trace_content = tuple(events)  # Convert the events to a hashable tuple
        if trace_content not in unique_traces:
            selected_trace_ids.append(trace_id)
            unique_traces[trace_content] = 1
        else:
            unique_traces[trace_content] += 1

    selected_traces = {
        trace_id: {
            "events": flattened_data[trace_id],
            "count": unique_traces[tuple(flattened_data[trace_id])]
        }
        for trace_id in selected_trace_ids
    }

    # Get the relevant trace IDs from selected_traces
    relevant_trace_ids = selected_traces.keys()

    # Filter log_csv to include only relevant traces
    filtered_log = log_csv[log_csv['case:concept:name'].isin(relevant_trace_ids)].copy()

    # Sort filtered_log based on unique event counts
    filtered_log['variant_count'] = filtered_log['case:concept:name'].map(
        {trace_id: trace_info['count'] for trace_id, trace_info in selected_traces.items()}
    )
    filtered_log.sort_values(by='variant_count', ascending=False, inplace=True)

    # Create a dictionary to map existing values to new IDs
    unique_values = filtered_log['case:concept:name'].unique()
    value_to_id = {value: i + 1 for i, value in enumerate(unique_values)}

    # Map the values in the 'case:concept:name' column to new IDs
    filtered_log['case:concept:name'] = filtered_log['case:concept:name'].map(value_to_id)

    return filtered_log

def create_custom_layout(log_csv, distribution, x_axis_label, x_tickformat, aggregation, selected):

    y_vals = list(range(1, len(log_csv['case:concept:name'].unique()) + 1))

    if selected == "Demo 1":
        height = 400
    elif selected == "Demo 2" and aggregation == "Cases":
        height = 3000
    else:
        height = 600

    if aggregation == "Cases":
        layout = go.Layout(
            title=f'{"Temporal" if distribution == "Time" else "Event sequence"} abstraction of aligned traces - Case-level',
            titlefont=dict(size=24),  # Set the font size of the general title (adjust as needed)
            xaxis=dict(
                title=x_axis_label,
                titlefont=dict(size=20),  # Set the font size of the x-axis title (adjust as needed)
                tickformat=x_tickformat,
                tickfont=dict(size=18),  # Set the font size of the x-axis tick labels (adjust as needed)
                showgrid=True,  # Show gridlines
                gridcolor='lightgray',  # Gridline color
            ),
            yaxis=dict(
                title='Case ID',
                titlefont=dict(size=20),  # Set the font size of the y-axis title (adjust as needed)
                tickvals=y_vals,
                ticktext=log_csv['case:concept:name'].unique(),
                showgrid=True,  # Show gridlines
                gridcolor='lightgray',  # Gridline color
                zeroline=False,  # Disable zero line
                ticksuffix='',  # Disable the default tick suffix (like 'e' in 1e6)
                range=[min(y_vals), max(y_vals)],  # Set the y-axis range based on your data
                tickfont=dict(size=18),  # Set the font size of the y-axis tick labels (adjust as needed)
            ),
            yaxis_autorange='reversed',
            hovermode='closest',
            plot_bgcolor='white',
            height=height,
        )
    else:

        variant_occurrences = log_csv[log_csv['event_count'] == 1]['variant_count']

        ticktext_list = [
            f"Variant {variant_num} ({occurrences} occurrences)"
            for variant_num, occurrences in zip(y_vals, variant_occurrences)
        ]

        layout = go.Layout(
            title=f'{"Temporal" if distribution == "Time" else "Event sequence"} abstraction of aligned traces - Variant-level',
            titlefont=dict(size=22),  # Set the font size of the general title (adjust as needed)
            xaxis=dict(
                title=x_axis_label,
                titlefont=dict(size=20),  # Set the font size of the x-axis title (adjust as needed)
                showgrid=True,  # Show gridlines
                gridcolor='lightgray',  # Gridline color
                tickformat=x_tickformat,
                tickfont=dict(size=18),  # Set the font size of the x-axis tick labels (adjust as needed)
            ),
            yaxis=dict(
                title='Variants',
                titlefont=dict(size=20),  # Set the font size of the y-axis title (adjust as needed)
                tickvals=y_vals,
                ticktext=ticktext_list,
                showgrid=True,  # Show gridlines
                gridcolor='lightgray',  # Gridline color
                zeroline=False,  # Disable zero line
                ticksuffix='',  # Disable the default tick suffix (like 'e' in 1e6)
                range=[min(y_vals), max(y_vals)],  # Set the y-axis range based on your data
                tickfont=dict(size=18),  # Set the font size of the y-axis tick labels (adjust as needed)
            ),
            yaxis_autorange='reversed',
            hovermode='closest',
            plot_bgcolor='white',
            height=height,
        )
    return layout, height

def find_deviations(log_csv, log, pn, im, fm):
    diagnostics = pm4py.conformance_diagnostics_alignments(log, pn, im, fm, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

    deviations_by_case = collect_deviations(diagnostics)
    log_csv_modified = missing_check(log_csv, deviations_by_case)
    log_csv_modified = deviation_check(log_csv_modified, deviations_by_case)

    return log_csv_modified

# Function to filter out tuples with None values in 'alignment'
def filter_alignment(alignment_list):
    return [(event, value) for event, value in alignment_list if value is not None]

def collect_deviations(diagnostics):

    filtered_diagnostics = [{k: filter_alignment(v) if k == 'alignment' else v for k, v in d.items()} for d in
                            diagnostics]
    deviations_by_case = {}
    current_case_id = 1

    for entry in filtered_diagnostics:
        alignment = entry['alignment']
        current_deviations = []
        current_event_id = 1

        for event, value in alignment:
            if event == '>>' or value == '>>':
                current_deviations.append((current_event_id, (event, value)))
            current_event_id += 1

        deviations_by_case[current_case_id] = current_deviations
        current_case_id += 1

    return deviations_by_case

def missing_check(log_csv, deviations_by_case):
    # Flatten the deviations_by_case dictionary to a list of tuples with case_id and deviation
    missing_events = {k: [(x, y) for x, y in v if y[0] == '>>'] for k, v in deviations_by_case.items()}
    missing_events = [(case_id, deviation) for case_id, deviations in missing_events.items() for deviation in
                      deviations]

    result_df = pd.DataFrame(columns=log_csv.columns)
    result_df['missing'] = None
    current_id = 1
    current_case_id = 1
    current_event_id = 1
    ticker = 0
    (alignment_case_id, (alignment_event_id, alignment)) = missing_events[0]

    for i, event in log_csv.iterrows():

        if event[0] != str(current_case_id):
            current_case_id = int(event[0])
            current_event_id = 1
            ticker = 0

        if str(alignment_case_id) == event[0] and alignment_event_id == (event[3] + ticker):
            result_df.loc[current_id] = [str(current_case_id), alignment[1], pd.Timestamp(None), current_event_id, True]
            missing_events.pop(0)
            if (len(missing_events) > 0):
                (alignment_case_id, (alignment_event_id, alignment)) = missing_events[0]
            current_event_id += 1
            current_id += 1
            ticker += 1
            result_df.loc[current_id] = event.tolist()[0:-1] + [current_event_id, False]
        else:
            result_df.loc[current_id] = event.tolist()[0:-1] + [current_event_id, False]

        current_event_id += 1
        current_id += 1

    while len(missing_events) > 0:
        (alignment_case_id, (alignment_event_id, alignment)) = missing_events[0]
        result_df.loc[current_id] = [str(current_case_id), alignment[1], pd.Timestamp(None), current_event_id, True]
        current_event_id += 1
        current_id += 1
        missing_events.pop(0)

    return result_df


def deviation_check(log_csv, deviations_by_case):
    # Flatten the deviations_by_case dictionary to a list of tuples with case_id and deviation
    deviations = {k: [(x, y) for x, y in v if y[1] == '>>'] for k, v in deviations_by_case.items()}
    deviations = [(case_id, deviation) for case_id, deviations in deviations.items() for deviation in deviations]

    # Create an empty DataFrame to store the result
    result_df = log_csv.copy()
    result_df['is_deviation'] = False

    for (alignment_case_id, (alignment_event_id, alignment)) in deviations:
        condition = (result_df['case:concept:name'] == str(alignment_case_id)) & (result_df['event_count'] == alignment_event_id)
        result_df.loc[condition, 'is_deviation'] = True

    return result_df

def save_variant_table(log, pn, im, fm):

    aligned_traces = pm4py.conformance_diagnostics_alignments(log, pn, im, fm)
    filtered_diagnostics = [{k: filter_alignment(v) if k == 'alignment' else v for k, v in d.items()} for d in aligned_traces]
    pm4py.save_vis_alignments(log, filtered_diagnostics, 'data/images/vis-alignments.svg')
    cairosvg.svg2png(url="data/images/vis-alignments.svg", write_to='data/images/vis-alignments.png', output_width=6000)


