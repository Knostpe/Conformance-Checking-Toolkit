import streamlit as st
from streamlit_option_menu import option_menu
import utils.util as Util
import utils.text_content as text_content
import components.run_dashboard as Dash


st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 0.5`')

st.sidebar.markdown('''
---
Created by [Knostpe](https://github.com/Knostpe).
''')

c1, c2, c3 = st.columns((2, 6, 2))

with c2:

    st.image('data/images/cctk_banner.png', use_column_width=True)

    st.header("Welcome to the Conformance Checking Toolkit")

    st.write(text_content.welcome_message)

    # Import and prepare data

    log = None
    pn = None

    # 2. horizontal menu
    selected = option_menu(None, ["Help Page", "Demo 1", "Demo 2", "Free Upload"],
        icons=['list-task', 'list-task','list-task', "cloud-upload"],
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selected == "Help Page":

            st.header("Everything you need to know to use CCTK")

            st.markdown('#### FAQ')
            with st.expander("What is **Process Mining**?"):
                st.write(text_content.process_mining_introduction, unsafe_allow_html=True)
            with st.expander("What is **Conformance Checking**?"):
                st.write(text_content.conformance_checking_introduction, unsafe_allow_html=True)
            with st.expander("What are (business) **process models**?"):
                st.write(text_content.business_process_model_introduction, unsafe_allow_html=True)
            with st.expander("What are **event logs**?"):
                st.write(text_content.event_logs_introduction, unsafe_allow_html=True)

            st.markdown('#### About the visual representations:')

            image_path_A = "data/images/metrics_info.png"  # Replace with the path to your image file
            image_path_B = "data/images/alignment_model_info.png"  # Replace with the path to your image file
            image_path_C = "data/images/alignment_log_info.png"  # Replace with the path to your image file
            image_path_D = "data/images/variant_table_info.png"  # Replace with the path to your image file
            image_path_E = "data/images/alignment_plot_info.png"  # Replace with the path to your image file

            with st.expander("How to interpret the **Metrics**"):
                st.image(image_path_A, caption="How to interpret the Metrics", use_column_width=True)
            with st.expander("How to interpret the **Alignment Model**"):
                st.image(image_path_B, caption="How to interpret the Alignment Model", use_column_width=True)
            with st.expander("How to interpret the **Alignment Log**"):
                st.image(image_path_C, caption="How to interpret the Alignment Log", use_column_width=True)
            with st.expander("How to interpret the **Variant Table**"):
                st.image(image_path_D, caption="How to interpret the Variant Table", use_column_width=True)
            with st.expander("How to interpret the **Alignment Plot**"):
                st.image(image_path_E, caption="How to interpret the Alignment Plot", use_column_width=True)

    if selected == "Demo 1":
        st.header("Illustration with an event log containing 6 cases")
    if selected == "Demo 2":
        st.header("Illustration with an event log containing 100 cases")
    if selected == "Free Upload":
        st.header("Try CCTK with your own event and model data!")

        c4, c5 = st.columns((3, 3))

        with c4:
            uploaded_log = st.file_uploader("Choose an event log")
            sep = ","

            if uploaded_log is not None:
                log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep)

                st.write(log_csv_show)

        with c5:
            uploaded_model = st.file_uploader("Choose a process model")

            if uploaded_model is not None:
                pn, im, fm, image1 = Util.get_model(uploaded_model)

                st.graphviz_chart(image1)
                # Util.model_viz(image1, zoom=1.5)

if selected == "Demo 1":
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

    uploaded_log = "data/bpi12/BPI_Challenge_2012_reduced_A.csv"
    sep = ","
    timestamp_format = "%Y-%m-%d %H:%M:%S.%f"

    log, log_csv, log_csv_show = Util.get_log(uploaded_log, sep, timestamp_format)

    uploaded_model = "bpi12_Model_A_fixed.pnml"
    pn_viz = "big"

    pn, im, fm = Util.get_model(uploaded_model)

    resulting_log_data = Util.find_deviations(log_csv, log, pn, im, fm)

    Dash.run_dashboard(log, pn, im, fm, log_csv_show, pn_viz, resulting_log_data)

if log is not None and pn is not None:

    #Util.plot_compare_calc(Util.fitness_compare_calc(log, pn, im, fm))

    scatter_plot = '''                                                                                                                                                     
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <h4><i class="fas fa-chart-bar"></i>  Alignment Plot</h4>
    '''

    st.write(scatter_plot, unsafe_allow_html=True)

    c1, c2, c3 = st.columns((3, 3, 3))

    with c1:
        distribution = st.radio("Choose the distribution:", ["Event ID", "Time"], horizontal=True)
    with c2:
        type = st.radio("Choose the highlighting options:", ["Deviation Type", "Event Type"], horizontal=True)
    with c3:
        aggregation = st.radio("Choose the aggregation:", ["Cases", "Variants"], horizontal=True)

    Util.plot_distribution(resulting_log_data, distribution, type, aggregation, selected)











