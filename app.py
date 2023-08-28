import streamlit as st
from streamlit_option_menu import option_menu
import pm4py
import utils.util as Util
import components.run_dashboard as Dash

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 0.3`')

st.sidebar.markdown('''
---
Created by [Knostpe](https://github.com/Knostpe).
''')

#st.image(Image.open('data/images/Process-Mining-banner.jpg'), width=400)

st.header("Welcome to the Conformance Checking Toolkit (CCTK) Prototype")

st.write("""
Dear Participants,

We greatly appreciate your willingness to participate in this research, which aims to evaluate the effectiveness of our prototype in supporting the representation of conformance checking results through visual analytics.

This toolkit has been developed with the purpose of helping users like you gain valuable insights from conformance checking data and make informed decisions to improve process efficiency and compliance. Your valuable feedback and experiences will play a pivotal role in refining and enhancing the toolkit's usability and functionality.

We kindly ask you to complete the survey and engage with the case study tasks provided in the prototype.Your inputs will contribute significantly to our research and will shape the toolkit's future development, ensuring it meets the needs of users in real-world scenarios.

Thank you for your time and commitment.Let's embark on this user study journey together to unlock the full potential of CCTK.
""")

with st.expander("What is Conformance Checking?"):
    st.write("""
    Conformance checking is a process used in the field of process mining and business process management to assess the alignment between observed process 
    behavior and the expected or intended behavior of a process. It involves comparing real-world execution traces of a process, often captured in event logs, 
    with a predefined process model or specification.

    The main goal of conformance checking is to identify and quantify discrepancies or deviations between the observed process executions and the expected 
    behavior. These discrepancies are often referred to as "violations" or "deviations" and can highlight potential inefficiencies, non-compliance with regulations, or 
    opportunities for process improvement.

    Conformance checking is an essential tool for organizations seeking to gain insights into their business processes' actual execution and identify 
    areas for optimization and compliance assurance. The results of conformance checking help process analysts and managers make data-driven decisions to 
    enhance process performance, identify bottlenecks, and ensure adherence to process standards.
    """)

with st.expander("What should be achieved through the CCTK Prototype?"):
    st.write("""
    This tool aims to empower you to gain valuable insights from conformance checking data and make data-driven decisions for process improvement and compliance. 
    Through this prototype, we strive to provide effective visual representations, result abstractions, decision-support features, and a user-centric experience 
    to enhance your understanding and analysis of conformance checking results.

    Thank you for your participation and valuable feedback.
    """)

with st.expander("What is the CCTK Prototype Roadmap?"):
    svg_string = Util.read_svg_file('data/images/CCTK Prototype Roadmap.svg')
    Util.render_svg(svg_string)

# Import and prepare data

log = None
pn = None

# 2. horizontal menu
selected = option_menu(None, ["Demo 1", "Demo 2", "Free Upload"],
    icons=['list-task', 'list-task','list-task', "cloud-upload"],
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Demo 1":
   st.header("Demo 1 - Example with a (small) event log of 6 cases")

   uploaded_log = "data/example/running_example_broken.csv"
   sep = ";"
   timestamp_format = "%Y-%m-%d %H:%M:%S"

   log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep, timestamp_format)

   uploaded_model = "running_example.pnml"
   pn_viz = "small"

   pn, im, fm = Util.get_model(uploaded_model)

   resulting_log_data = Util.find_deviations(log_csv, log, pn, im, fm)

   Dash.run_dashboard(log, pn, im, fm, log_csv_show, pn_viz, resulting_log_data)

if selected == "Demo 2":
    st.header("Demo 2 - Example with a (big) event log of 100 cases")

    uploaded_log = "data/bpi12/BPI_Challenge_2012_reduced_A.csv"
    sep = ","
    timestamp_format = "%Y-%m-%d %H:%M:%S.%f"

    log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep, timestamp_format)

    uploaded_model = "bpi12_Model_A_fixed.pnml"
    pn_viz = "big"

    pn, im, fm = Util.get_model(uploaded_model)

    resulting_log_data = Util.find_deviations(log_csv, log, pn, im, fm)

    Dash.run_dashboard(log, pn, im, fm, log_csv_show, pn_viz, resulting_log_data)

if selected == "Free Upload":
   st.header("Free Upload - Try CCTK with your own event and model data!")

   c1, c2 = st.columns((5, 5))

   with c1:
       st.markdown('### Event Log')

       uploaded_log = st.file_uploader("Choose an event log")
       sep = ","

       if uploaded_log is not None:

           log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep)

           st.write(log_csv_show)

   with c2:
       st.markdown('### Process Model')

       uploaded_model = st.file_uploader("Choose a process model")

       if uploaded_model is not None:

            pn, im, fm, image1 = Util.get_model(uploaded_model)

            st.graphviz_chart(image1)
            #Util.model_viz(image1, zoom=1.5)

if log is not None and pn is not None:

   st.markdown('#### Break-down and compare conformance')

   Util.plot_compare_calc(Util.fitness_compare_calc(log, pn, im, fm))

   st.markdown('##### Case-Model representation')

   type = st.radio("Event highlighting options:",
                   ["Highlight Missing and Deviating Events", "Highlight by Event Types"], horizontal=True)
   distribution = st.radio("Choose the distribution:", ["Event Number", "Time"], horizontal=True)
   if distribution == "Event Number" and type == "Highlight Missing and Deviating Events":
       Util.plot_distribution(resulting_log_data, show_deviations=True)
   elif distribution == "Event Number" and type == "Highlight by Event Types":
       Util.plot_distribution(resulting_log_data, color_by_event_type=True)
   elif distribution == "Time" and type == "Highlight Missing and Deviating Events":
       Util.plot_distribution(resulting_log_data, x_axis='time', show_deviations=True)
   elif distribution == "Time" and type == "Highlight by Event Types":
       Util.plot_distribution(resulting_log_data, x_axis='time', color_by_event_type=True)

   st.markdown('##### Variant-Model representation')

   aligned_traces = pm4py.conformance_diagnostics_alignments(log, pn, im, fm)
   filtered_diagnostics = [{k: Util.filter_alignment(v) if k == 'alignment' else v for k, v in d.items()} for d in aligned_traces]
   pm4py.save_vis_alignments(log, filtered_diagnostics, 'data/images/vis-alignments.svg')
   svg_string = Util.read_svg_file('data/images/vis-alignments.svg')
   Util.render_svg(svg_string, height="1000px", open_in_new_tab=True)

   st.markdown('#### Alignment Log')
   st.write(resulting_log_data)






