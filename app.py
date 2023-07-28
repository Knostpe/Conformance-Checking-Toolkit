import streamlit as st
import pandas as pd
from PIL import Image
import pm4py
import utils.util as Util

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('CCTK `version 0.1`')

st.sidebar.subheader('Conformance Checking Settings')

roadmap = st.sidebar.selectbox('Show roadmap', ('no', 'yes'))

addmodel = st.sidebar.selectbox('Show additional model representations', ('none', 'frequency', 'performance'))

algorithm = st.sidebar.selectbox('Select algorithm', ('alignment', 'token replay'))

abstraction = st.sidebar.selectbox('Select abstraction level', ('log-model', 'variant-model', 'case-model'))

st.sidebar.markdown('''
---
Created by [Knostpe](https://github.com/Knostpe).
''')

if roadmap == 'yes':
    svg_string = Util.read_svg_file('data/images/CCTK Prototype Roadmap.svg')
    Util.render_svg(svg_string)

# Import and prepare data

log = None
pn = None

c1, c2 = st.columns((5,5))
with c1:
    st.markdown('### Event Log')

    uploaded_log = st.file_uploader("Choose an event log")

    if uploaded_log is not None:
        # Can be used wherever a "file-like" object is accepted:
        log_csv = pm4py.format_dataframe(pd.read_csv(uploaded_log, sep=';'), case_id='case:concept:name',
                                     activity_key='concept:name', timestamp_key='time:timestamp')

        # Row A
        st.write(log_csv)
        log = pm4py.convert_to_event_log(log_csv)
with c2:
    st.markdown('### Process Model')


#    if discover == 'no':
    uploaded_model = st.file_uploader("Choose a process model")
    if uploaded_model is not None:
        pn, im, fm = pm4py.read_pnml('data/models/' + uploaded_model.name)
        try:
            image1 = Image.open('data/images/' + uploaded_model.name[:-4] + 'png')
        except FileNotFoundError:
            pm4py.save_vis_petri_net(pn, im, fm, 'data/images/' + uploaded_model.name[:-4] + 'png')
            image1 = Image.open('data/images/' + uploaded_model.name[:-4] + 'png')
        Util.model_viz(image1, zoom=1.5)

if log is not None and pn is not None:

    if addmodel == 'frequency':
        st.markdown('### Frequency')
        Util.frequency_viz(log, pn, im, fm)

    if addmodel == 'performance':
        st.markdown('### Performance')
        Util.performance_viz(log, pn, im, fm)

    st.markdown('### Conformance Checking Results')

    st.markdown('##### Quantify conformance')
    fitness = Util.fitness_calc(algorithm, log, pn, im, fm)
    Util.fitness_viz(fitness)

    st.markdown('##### Break-down and compare conformance')

    Util.plot_compare_calc(Util.fitness_compare_calc(algorithm,log, pn, im, fm))

    st.markdown('##### Localize and show deviations')

    if abstraction == 'log-model' and algorithm == 'alignment':

        Util.alignment_viz(log, pn, im, fm)

    elif abstraction == 'log-model' and algorithm == 'token replay':

        st.markdown('#### TODO')
        image2 = Image.open('data/images/template_localize and show_petri net.png')
        Util.model_viz(image2)

    elif abstraction == 'variant-model'and algorithm == 'token replay':

        st.markdown('#### TODO')
        image2 = Image.open('data/images/template_localize and show_traces.png')
        Util.model_viz(image2)

    elif abstraction == 'variant-model' and algorithm == 'alignment':

        aligned_traces = pm4py.conformance_diagnostics_alignments(log, pn, im, fm)
        pm4py.save_vis_alignments(log, aligned_traces, 'data/images/vis-alignments.svg')
        svg_string = Util.read_svg_file('data/images/vis-alignments.svg')
        Util.render_svg(svg_string, height="400px", open_in_new_tab=True)

