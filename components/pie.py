import json

from streamlit_elements import nivo, mui
from .dashboard import Dashboard


class Pie(Dashboard.Item):

    def generate_data(values):
        categories = ["Conformant Events", "Deviating Events", "Missing Events"]
        colors = ["hsl(128, 70%, 50%)", "hsl(178, 70%, 50%)", "hsl(322, 70%, 50%)"]

        data = []
        for i, category in enumerate(categories):
            data.append({
                "id": category,
                "label": category.split()[0],
                "value": values[i],
                "color": colors[i]
            })

        return json.dumps(data, indent=2)

    DEFAULT_DATA = [
        {"id": "Conformant Events", "label": "Conformant", "value": 10, "color": "hsl(128, 70%, 50%)"},
        {"id": "Deviating Events", "label": "Deviating", "value": 10, "color": "hsl(178, 70%, 50%)"},
        { "id": "Missing Events", "label": "Missing", "value": 10, "color": "hsl(322, 70%, 50%)"}
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, json_data):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.icon.PieChart()
                mui.Typography("Pie chart", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Pie(
                    data=data,
                    theme=self._theme["light"],
                    margin={ "top": 40, "right": 80, "bottom": 80, "left": 80 },
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                0.2,
                            ]
                        ]
                    },
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="grey",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={ "from": "color" },
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                2
                            ]
                        ]
                    },
                    defs=[
                        {
                            "id": "dots",
                            "type": "patternDots",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "size": 4,
                            "padding": 1,
                            "stagger": True
                        },
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10
                        }
                    ],
                    fill=[
                        { "match": { "id": "ruby" }, "id": "dots" },
                        { "match": { "id": "c" }, "id": "dots" },
                        { "match": { "id": "go" }, "id": "dots" },
                        { "match": { "id": "python" }, "id": "dots" },
                        { "match": { "id": "scala" }, "id": "lines" },
                        { "match": { "id": "lisp" }, "id": "lines" },
                        { "match": { "id": "elixir" }, "id": "lines" },
                        { "match": { "id": "javascript" }, "id": "lines" }
                    ],
                    legends=[
                        {
                            "anchor": "bottom",
                            "direction": "row",
                            "justify": False,
                            "translateX": 0,
                            "translateY": 56,
                            "itemsSpacing": 0,
                            "itemWidth": 100,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolSize": 18,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )