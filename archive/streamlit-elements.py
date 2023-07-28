from streamlit_elements import elements, mui, html, lazy, sync, editor
import streamlit as st
import streamlit.components.v1 as components
import json

import pandas as pd
from PIL import Image
import pm4py
import utils.util as Util

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 1`')

st.sidebar.subheader('Conformance Checking Settings')
discover = st.sidebar.selectbox('Select discover option', ('no', 'yes'))

algorithm = st.sidebar.selectbox('Select algorithm', ('token replay', 'alignment'))

model = st.sidebar.selectbox('Select model view TODO', ('petri net', 'BPMN'))

abstraction = st.sidebar.selectbox('Select abstraction level TODO', ('log-model', 'variant-model', 'case-model'))

compare = st.sidebar.selectbox('Select compare options TODO', ('variants', 'time', 'xyz'))

view = st.sidebar.selectbox('Select process constraint TODO', ('control-flow', 'data'))

st.sidebar.markdown('''
---
Created by [Knostpe](https://github.com/Knostpe).
''')

# Import and prepare data

log = None
pn = None

c1, c2 = st.columns((5,5))
with c1:
    st.markdown('### Event Log')

    uploaded_log = st.file_uploader("Choose an event log")

    if uploaded_log is not None:
        # Can be used wherever a "file-like" object is accepted:
        log = pm4py.format_dataframe(pd.read_csv(uploaded_log, sep=';'), case_id='case:concept:name',
                                     activity_key='concept:name', timestamp_key='time:timestamp')
        # , case_id = 'case_id', activity_key = 'activity', timestamp_key = 'timestamp' clean
        # , case_id = 'case:concept:name', activity_key = 'concept:name', timestamp_key = 'time:timestamp' dirty

        # Row A
        st.write(log)
with c2:
    st.markdown('### Process Model')

    if discover == 'no':
        uploaded_model = st.file_uploader("Choose a process model")
        if uploaded_model is not None:
            pn, im, fm = pm4py.read_pnml('data/models/' + uploaded_model.name)

            # Save and read graph as HTML file (locally)
            #pm4py.save_vis_petri_net(pn, im, fm, 'data/images/petri_net.png')
            #pm4py.view_petri_net(pn, im, fm, format='html')

            HtmlFile = open('data/html/petri_net.html', 'r', encoding='utf-8')

            # Load HTML file in HTML component for display on Streamlit page
            components.html(HtmlFile.read(), height=435)


    if discover == 'yes' and log is not None:
        pn, im, fm = pm4py.discover_petri_net_inductive(log)
        pm4py.save_vis_petri_net(pn, im, fm, 'data/images/petri_net.png')
        image1 = Image.open('data/images/petri_net.png')


if log is not None and pn is not None:
    st.markdown('### Conformance Checking Results')

    st.markdown('##### Quantify conformance')
    fitness = Util.fitness_calc(algorithm, log, pn, im, fm)
    Util.fitness_viz(fitness)

    st.markdown('##### Localize and show deviations (TODO)')

    if model == 'petri net' and abstraction == 'log-model':
        image2 = Image.open('data/images/template_localize and show_petri net.png')
    elif abstraction == 'variant-model' or abstraction == 'case-model':
        image2 = Image.open('data/images/template_localize and show_traces.png')
    elif model == 'BPMN' and abstraction == 'log-model':
        image2 = Image.open('data/images/template_localize and show_bpmn.png')
    else:
        image2 = Image.open('data/images/petri_net.png')

    Util.model_viz(image2)

with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        # isDraggable=False, moved=False
        dashboard.Item("first_item", 0, 0, 6, 3),
        dashboard.Item("second_item", 6, 0, 6, 3),
        dashboard.Item("third_item", 0, 3, 12, 3),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item", key="second_item")
        mui.Paper("Third item", key="second_item")

#HtmlFile


