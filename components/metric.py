from streamlit_elements import mui
from .dashboard import Dashboard


class Metric(Dashboard.Item):

    def __call__(self, text):
        lst = str(text).split(";")

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.Numbers()
                mui.Typography(lst[0])

            # Center the image and add padding for CardMedia
            with mui.Box(sx={"display": "flex", "justifyContent": "center", "padding": "20px"}):
                mui.Typography(lst[1], variant="h4")