import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from . import Dashboard, DataGrid, Model, Metric, Pie
from utils import util as Util

def run_dashboard(log, pn, im, fm, log_csv_show, pn_viz, resulting_log_data):

    board = Dashboard()
    w = SimpleNamespace(
        dashboard=board,
        event_log=DataGrid(board, 0, 0, 6, 6, minW=3, minH=3),
        proces_model=Model(board, 6, 0, 6, 6, minW=3, minH=3),
        metric1=Metric(board, 0, 6, 2.5, 3, minW=2, minH=2),
        metric2=Metric(board, 2.5, 6, 2.5, 3, minW=2, minH=2),
        metric3=Metric(board, 5, 6, 2.5, 3, minW=2, minH=2),
        metric4=Metric(board, 0, 9, 2.5, 3, minW=2, minH=2),
        metric5=Metric(board, 2.5, 9, 2.5, 3, minW=2, minH=2),
        metric6=Metric(board, 5, 9, 2.5, 3, minW=2, minH=2),
        pie=Pie(board, 7.5, 6, 4.5, 6, minW=3, minH=4),
    )
    state.w = w

    # Add a unique 'id' column based on row index
    log_csv_show['id'] = log_csv_show.index + 1

    # Convert DataFrame to a list of dictionaries
    log_csv_show_as_dict = log_csv_show.to_dict(orient='records')

    metrics123 = Util.fitness_calc(log, pn, im, fm)



    metrics456 = [len(resulting_log_data[(~resulting_log_data['missing']) & (~resulting_log_data['is_deviation'])]),
              len(resulting_log_data[resulting_log_data['is_deviation']]),
              len(resulting_log_data[resulting_log_data['missing']])]


    w.dashboard.add_tab("Event Log", json.dumps(log_csv_show_as_dict, indent=2), "json")
    w.dashboard.add_tab("Process Model", pn_viz, "plaintext")
    w.dashboard.add_tab("Log Fitness", "Log Fitness;"+str(round(metrics123['log_fitness'], 2)), "plaintext")
    w.dashboard.add_tab("Avg Trace Fitness", "Avg Trace Fitness;"+str(round(metrics123['average_trace_fitness'], 2)), "plaintext")
    w.dashboard.add_tab("% of Fitting Traces", "% of Fitting Traces;"+str(round(metrics123['percentage_of_fitting_traces'], 2)), "plaintext")
    w.dashboard.add_tab("Conformant Events", "Conformant Events;"+str(metrics456[0]), "plaintext")
    w.dashboard.add_tab("Deviating Events", "Deviating Events;"+str(metrics456[1]), "plaintext")
    w.dashboard.add_tab("Missing Events", "Missing Events;"+str(metrics456[2]), "plaintext")
    w.dashboard.add_tab("Pie", Pie.generate_data(metrics456), "json")

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.event_log(w.dashboard.get_content("Event Log"))
            w.proces_model(w.dashboard.get_content("Process Model"))
            w.metric1(w.dashboard.get_content("Log Fitness"))
            w.metric2(w.dashboard.get_content("Avg Trace Fitness"))
            w.metric3(w.dashboard.get_content("% of Fitting Traces"))
            w.metric4(w.dashboard.get_content("Conformant Events"))
            w.metric5(w.dashboard.get_content("Deviating Events"))
            w.metric6(w.dashboard.get_content("Missing Events"))
            w.pie(w.dashboard.get_content("Pie"))


