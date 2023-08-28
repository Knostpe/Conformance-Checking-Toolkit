from streamlit_elements import mui
from .dashboard import Dashboard
from PIL import Image as PILImage
from io import BytesIO
import streamlit as st
from PIL import Image
from base64 import b64encode


class Model(Dashboard.Item):

    def __call__(self, text):

        lst = str(text).split(";")

        image_path = "https://raw.githubusercontent.com/Knostpe/thesis-test/master/data/images/" + lst[1]

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.AccountTree()
                mui.Typography(lst[0])

            # Center the image and add padding for CardMedia
            with mui.Box(sx={"display": "flex", "justifyContent": "center", "padding": "20px"}):
                mui.CardMedia(
                    component="img",
                    sx={"maxWidth": "100%", "maxHeight": "100%", "width": "auto", "height": "auto"},
                    image=image_path,  # Pass the image bytes
                    alt="Image Alt Text",
                )
