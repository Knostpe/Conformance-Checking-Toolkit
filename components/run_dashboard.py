import json
import pandas as pd
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from . import Dashboard, DataGrid, DataGridAlign, Model, Metric, Pie
from utils import util as Util

def run_dashboard(log, pn, im, fm, log_csv_show, pn_viz, resulting_log_data):

    if (pn_viz == "small"):
        height = 6
    else:
        height = 10

    board = Dashboard()
    w = SimpleNamespace(
        dashboard=board,
        proces_model=Model(board, 0, 0, 6, 9, minW=3, minH=3),
        event_log=DataGrid(board, 6, 0, 6, 9, minW=3, minH=3),
        metric1=Metric(board, 0, 9, 2, 3, minW=2, minH=2),
        metric2=Metric(board, 2, 9, 2, 3, minW=2, minH=2),
        metric3=Metric(board, 4, 9, 2, 3, minW=2, minH=2),
        metric4=Metric(board, 0, 12, 2, 3, minW=2, minH=2),
        metric5=Metric(board, 2, 12, 2, 3, minW=2, minH=2),
        metric6=Metric(board, 4, 12, 2, 3, minW=2, minH=2),
        pie=Pie(board, 6, 9, 6, 6, minW=3, minH=4),
        alignment_model=Model(board, 0, 15, 6, 9, minW=3, minH=3),
        alignment_log=DataGridAlign(board, 6, 15, 6, 9, minW=3, minH=3),
        variant_table=Model(board, 0, 24, 12, height, minW=3, minH=3),
    )
    state.w = w

    metrics123 = Util.fitness_calc(log, pn, im, fm)

    metrics456 = [len(resulting_log_data[(~resulting_log_data['missing']) & (~resulting_log_data['is_deviation'])]),
              len(resulting_log_data[resulting_log_data['is_deviation']]),
              len(resulting_log_data[resulting_log_data['missing']])]

    # Add a unique 'id' column based on row index
    log_csv_show['id'] = log_csv_show.index + 1

    alignment_log = resulting_log_data.copy()
    alignment_log = alignment_log.rename(columns={'case:concept:name': 'CaseID', 'concept:name': 'Event Type', 'time:timestamp': 'Timestamp', 'event_count': 'EventID', 'is_deviation': 'Deviating', 'missing': 'Missing'})
    alignment_log['id'] = alignment_log.index + 1
    alignment_log["Timestamp"] = pd.to_datetime(alignment_log["Timestamp"], format='mixed')
    if (pn_viz == "small"):
        alignment_log["Timestamp"] = alignment_log["Timestamp"].dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        alignment_log["Timestamp"] = alignment_log["Timestamp"].dt.strftime('%Y-%m-%d %H:%M:%S.%f')


    w.dashboard.add_tab("Event Log", json.dumps(log_csv_show.to_dict(orient='records'), indent=2), "json")
    w.dashboard.add_tab("Process Model", "Process Model;petri_net_"+pn_viz+".png", "plaintext")
    w.dashboard.add_tab("Log Fitness", "Log Fitness;"+str(round(metrics123['log_fitness'], 2)), "plaintext")
    w.dashboard.add_tab("Avg Trace Fitness", "Avg Trace Fitness;"+str(round(metrics123['average_trace_fitness'], 2)), "plaintext")
    w.dashboard.add_tab("Fitting Traces", "Fitting Traces;"+str(round(metrics123['percentage_of_fitting_traces'], 2))+" %", "plaintext")
    w.dashboard.add_tab("Conformant Events", "Conformant Events;"+str(metrics456[0]), "plaintext")
    w.dashboard.add_tab("Deviating Events", "Deviating Events;"+str(metrics456[1]), "plaintext")
    w.dashboard.add_tab("Missing Events", "Missing Events;"+str(metrics456[2]), "plaintext")
    w.dashboard.add_tab("Pie", Pie.generate_data(metrics456), "json")
    w.dashboard.add_tab("Alignment Model", "Alignment Model;alignment_viz_"+pn_viz+".png", "plaintext")
    w.dashboard.add_tab("Alignment Log", json.dumps(alignment_log.to_dict(orient='records'), indent=2), "json")
    w.dashboard.add_tab("Variant Table", "Variant Table;vis-alignments_"+pn_viz+".png", "plaintext")

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.event_log(w.dashboard.get_content("Event Log"))
            w.proces_model(w.dashboard.get_content("Process Model"))
            w.metric1(w.dashboard.get_content("Log Fitness"))
            w.metric2(w.dashboard.get_content("Avg Trace Fitness"))
            w.metric3(w.dashboard.get_content("Fitting Traces"))
            w.metric4(w.dashboard.get_content("Conformant Events"))
            w.metric5(w.dashboard.get_content("Deviating Events"))
            w.metric6(w.dashboard.get_content("Missing Events"))
            w.pie(w.dashboard.get_content("Pie"))
            w.alignment_model(w.dashboard.get_content("Alignment Model"))
            w.alignment_log(w.dashboard.get_content("Alignment Log"))
            w.variant_table(w.dashboard.get_content("Variant Table"))

