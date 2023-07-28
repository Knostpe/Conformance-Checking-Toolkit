import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pm4py
from pm4py.visualization.petri_net import visualizer as vis
from pm4py.visualization.petri_net.variants import token_decoration_frequency as tdf
from pm4py.visualization.petri_net.variants import token_decoration_performance as tdp
import base64

def model_viz(image, zoom=None):
    """Displays the given image with optional size and zoom customization."""
    st.image(image)


def fitness_calc(algorithm, log, pn, im, fm):
    if algorithm == 'alignment':
        fitness = pm4py.fitness_token_based_replay(log, pn, im, fm)
    elif algorithm == 'token replay':
        fitness = pm4py.fitness_alignments(log, pn, im, fm)
    else:
        fitness = None
    return fitness

def fitness_compare_calc(algorithm, log, pn, im, fm):

    fitness_df = None

    if algorithm == 'alignment':
        alignment_result = pm4py.conformance_diagnostics_alignments(log, pn, im, fm)

        alignment_fitness = {}
        for i, trace in enumerate(alignment_result):
            fitness_value = trace['fitness']
            case_id = f'Case {i + 1}'
            alignment_fitness[case_id] = fitness_value

        fitness_df = pd.DataFrame.from_dict(alignment_fitness, orient='index', columns=['Alignment Fitness'])

    if algorithm == 'token replay':
        token_replay_result = pm4py.conformance_diagnostics_token_based_replay(log, pn, im, fm)

        token_replay_fitness = {}
        for i, trace in enumerate(token_replay_result):
            fitness_value = trace['trace_fitness']
            case_id = f'Case {i + 1}'
            token_replay_fitness[case_id] = fitness_value

        fitness_df = pd.DataFrame.from_dict(token_replay_fitness, orient='index', columns=['Token Replay Fitness'])

    return fitness_df

def alignment_viz(log, pn, im, fm):
    pn_decorated_align = vis.apply(pn, im, fm, log, variant=vis.ALIGNMENTS)
    st.graphviz_chart(pn_decorated_align)

def frequency_viz(log, pn, im, fm):
    pn_decorated_freq = tdf.apply(pn, im, fm, log)
    st.graphviz_chart(pn_decorated_freq)

def performance_viz(log, pn, im, fm):
    pn_decorated_perf = tdp.apply(pn, im, fm, log)
    st.graphviz_chart(pn_decorated_perf)

def fitness_viz(fitness):
    col1, col2, col3 = st.columns(3)
    col1.metric("Log Fitness", round(fitness['log_fitness'], 2), "")
    col2.metric("Avg Trace Fitness", round(fitness['average_trace_fitness'], 2), "")
    col3.metric("% of Fitting Traces", round(fitness['percentage_of_fitting_traces'], 2), "")

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

    # Define custom colors for markers
    marker_color = 'blue'

    # Create the scatter trace
    scatter_trace = go.Scatter(
        x=df.index,
        y=df[column_name],
        mode='markers',
        marker=dict(color=marker_color),
    )

    # Create the layout
    layout = go.Layout(
        title='Fitness distribution',
        xaxis=dict(title='Case ID'),
        yaxis=dict(title=column_name),
        hovermode='closest',
        plot_bgcolor='white',
    )

    # Create the figure and add the scatter trace
    fig = go.Figure(data=[scatter_trace], layout=layout)

    # Update marker style
    fig.update_traces(marker=dict(size=10, symbol='circle', line=dict(width=1, color=marker_color)))

    # Update axis style
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')

    # Update title style
    fig.update_layout(title_font=dict(size=16, family='Arial', color='black')) #IBM Plex Sans

    # Display the Plotly figure
    st.plotly_chart(fig)