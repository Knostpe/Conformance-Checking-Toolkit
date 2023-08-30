import streamlit as st
from streamlit_option_menu import option_menu
import pm4py
import utils.util as Util
import components.run_dashboard as Dash
import cairosvg


st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 0.3`')

st.sidebar.markdown('''
---
Created by [Knostpe](https://github.com/Knostpe).
''')

#st.image(Image.open('data/images/Process-Mining-banner.jpg'), width=400)

st.header("Welcome to the Conformance Checking Toolkit Prototype")

st.write("""
Dear Participants,

We appreciate your willingness to participate in this research, which aims to assess the effectiveness of our prototype in supporting the visual representation of conformance checking results.

The prototype was created to aid users in extracting insights from conformance checking data. 
When using visual analytics in the context of conformance checking, your feedback will be critical in understanding user expectations.

Please complete the survey, which should still be open in another tab, and participate in the tasks provided. Thank you for your time and effort.
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

# Import and prepare data

log = None
pn = None

# 2. horizontal menu
selected = option_menu(None, ["Demo 1", "Demo 2", "Free Upload"],
    icons=['list-task', 'list-task','list-task', "cloud-upload"],
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Demo 1":
   st.header("Illustration of the Prototype with an Example Event Log of 6 Cases")

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
    st.header("Illustration of the Prototype with an Example Event Log of 100 Cases")

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

    #Util.plot_compare_calc(Util.fitness_compare_calc(log, pn, im, fm))

    st.markdown('#### Scatter plot')
    c1, c2, c3 = st.columns((3, 3, 3))

    with c1:
        distribution = st.radio("Choose the distribution:", ["Event ID", "Time"], horizontal=True)
    with c2:
        type = st.radio("Choose the highlighting options:", ["Deviation Type", "Event Type"], horizontal=True)
    with c3:
        aggregation = st.radio("Choose the aggregation:", ["Variants", "Cases"], horizontal=True)

    Util.plot_distribution(resulting_log_data, distribution, type, aggregation, selected)











