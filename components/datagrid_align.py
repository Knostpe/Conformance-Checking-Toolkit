import json

from streamlit_elements import mui
from .dashboard import Dashboard


class DataGridAlign(Dashboard.Item):

    DEFAULT_COLUMNS = [
        {"field": 'CaseID', "headerName": 'Case ID', "type": 'number', "width": 65},
        {"field": 'Event Type', "headerName": 'Event Type', "width": 150, "editable": True},
        {"field": 'Timestamp', "headerName": 'Timestamp', "width": 170, "editable": True},
        {"field": 'EventID', "headerName": 'Event ID', "type": 'number', "width": 70, "editable": True},
        {"field": 'Deviating', "headerName": 'Deviating', "type": 'boolean', "width": 75, "editable": True},
        {"field": 'Missing', "headerName": 'Missing', "type": 'boolean', "width": 65, "editable": True},
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
                mui.Typography("Alignment Log")

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
