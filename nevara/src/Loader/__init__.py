from langchain_core.messages import HumanMessage
from pathlib import Path
import mimetypes
import base64

class ImageLoader:
    def __init__(self):
        self.res_dir = Path("./res").absolute()

    def _load_images(self):
        files = self.res_dir.glob('*')
        images: list[Path] = []
        for img in files:
            if img.suffix.lower() in [".png", ".jpg", ".jpeg"]: images.append(img)

        self.images = images

    def apply_images(self, message: HumanMessage):
        self._load_images()

        for img in self.images:
            mimetype, _ = mimetypes.guess_type(img.name)
            image_data = base64.b64encode(img.read_bytes()).decode("utf-8")
            if type(message.content) == str:                
                message = HumanMessage(
                    content=[
                        { 'type': 'text', 'text': message.content },
                        { 'type': 'image_url', 'image_url': { 'url': f"data:{mimetype};base64,{image_data}" } }
                    ]
                )
            if isinstance(message.content, list):
                message.content += [{ 'type': 'image_url', 'image_url': {'url': f'data:{mimetype};base64,{image_data}'} }]

        return message