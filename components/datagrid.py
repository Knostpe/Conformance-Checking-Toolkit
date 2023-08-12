import json

from streamlit_elements import mui
from .dashboard import Dashboard


class DataGrid(Dashboard.Item):

    DEFAULT_COLUMNS = [
        {"field": 'CaseID', "headerName": 'Case ID', "width": 90},
        {"field": 'Event Type', "headerName": 'Event Type', "width": 150, "editable": True},
        {"field": 'Timestamp', "headerName": 'Timestamp', "width": 150, "editable": True},
        {"field": 'EventID', "headerName": 'Event ID', "type": 'number', "width": 110, "editable": True},
    ]

    def _handle_edit(self, params):
        print(params)

    def __call__(self, json_data):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_ROWS

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.ViewCompact()
                mui.Typography("Event Log")

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=self.DEFAULT_COLUMNS,
                    rows=data,
                    pageSize=10,
                    rowsPerPageOptions=[10],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )



