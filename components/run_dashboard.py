import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from . import Dashboard, DataGrid, Model

def run_dashboard(log_csv_show = None, image = None):

    board = Dashboard()
    w = SimpleNamespace(
        dashboard=board,
        event_log=DataGrid(board, 0, 0, 6, 8, minW=3, minH=3),
        proces_model=Model(board, 6, 0, 6, 8, minH=5),
    )
    state.w = w

    # Add a unique 'id' column based on row index
    log_csv_show['id'] = log_csv_show.index + 1

    # Convert DataFrame to a list of dictionaries
    log_csv_show_as_dict = log_csv_show.to_dict(orient='records')

    w.dashboard.add_tab("Event Log", json.dumps(log_csv_show_as_dict, indent=2), "json")
    w.dashboard.add_tab("Process Model", image, "plaintext")


    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.event_log(w.dashboard.get_content("Event Log"))
            w.proces_model(w.dashboard.get_content("Process Model"))


