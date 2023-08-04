#from streamlit_elements import elements, mui, html, lazy, sync, editor
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import pandas as pd
from PIL import Image
import pm4py
import utils.util as Util

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 0.2`')

st.sidebar.subheader('Conformance Checking Settings')
#discover = st.sidebar.selectbox('Select discover option', ('no', 'yes'))

tab = st.sidebar.selectbox("Select a tab", ["Demo with small Dataset", "Demo with big Dataset", "Free Upload"])

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

tab1, tab2, tab3 = st.tabs(["Demo with small Dataset", "Demo with big Dataset", "Free Upload"])

with tab1:
    if tab == "Demo with small Dataset":
       st.header("Demo with small dataset")

       c1, c2 = st.columns((5, 5))

       with c1:
           st.markdown('### Event Log')

           uploaded_log = "data/example/running_example_broken.csv"
           sep = ";"
           timestamp_format = "%Y-%m-%d %H:%M:%S"

           log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep, timestamp_format)

           st.write(log_csv_show)

       with c2:
           st.markdown('### Process Model')

           uploaded_model = "running_example.pnml"

           pn, im, fm, image1 = Util.get_model(uploaded_model)

           Util.model_viz(image1, zoom=1.5)

with tab2:
    if tab == "Demo with big Dataset":
       st.header("Demo with big dataset")

       c1, c2 = st.columns((5, 5))

       with c1:
           st.markdown('### Event Log')

           uploaded_log = "data/bpi12/BPI_Challenge_2012_reduced.csv"
           sep = ","
           timestamp_format = "%Y-%m-%d %H:%M:%S.%f"

           log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep, timestamp_format)

           st.write(log_csv_show)

       with c2:
           st.markdown('### Process Model')

           uploaded_model = "bpi12_Model_AO_fixed.pnml"

           pn, im, fm, image1 = Util.get_model(uploaded_model)

           Util.model_viz(image1, zoom=1.5)
with tab3:
    if tab == "Free Upload":
       st.header("Free upload")

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

                Util.model_viz(image1, zoom=1.5)

if log is not None and pn is not None:

   st.markdown('### Conformance Checking Results')

   st.markdown('#### Alignment Log')
   resulting_log_data = Util.find_deviations(log_csv, pn, im, fm)
   st.write(resulting_log_data)

   st.markdown('#### Quantify conformance')
   fitness = Util.fitness_calc(log, pn, im, fm)
   Util.fitness_viz(fitness)

   st.markdown('#### Break-down and compare conformance')

   Util.plot_compare_calc(Util.fitness_compare_calc(log, pn, im, fm))

   st.markdown('#### Localize and show deviations')

   st.markdown('##### Log-Model representation')

   Util.alignment_viz(log, pn, im, fm)

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
   pm4py.save_vis_alignments(log, aligned_traces, 'data/images/vis-alignments.svg')
   svg_string = Util.read_svg_file('data/images/vis-alignments.svg')
   Util.render_svg(svg_string, height="400px", open_in_new_tab=True)