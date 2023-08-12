from streamlit_elements import mui
from .dashboard import Dashboard
from PIL import Image as PILImage
from io import BytesIO
from base64 import b64encode


class Model(Dashboard.Item):

    def __call__(self, image):
        if isinstance(image, PILImage.Image):
            # Convert PIL Image to bytes for display
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")

            # Encode these bytes to base 64.
            images_b64 = [b64encode(bytes).decode() for bytes in image_bytes]

            # Construct the path to the image within the data directory
            image_path = "https://github.com/Knostpe/thesis-test/blob/master/data/images/running_example.png?raw=true"

            with mui.Paper(key=self._key,
                           sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                           elevation=1):
                with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                    mui.icon.AccountTree()
                    mui.Typography("Process Model")

                mui.CardMedia(
                    component="img",
                    height=300,  # Adjust the height as needed
                    image=image_path,  # Pass the image bytes
                    alt="Image Alt Text",
                )

        else:
            raise ValueError("Input must be a PIL Image object")
