import base64


class ImageEncoder:
    @staticmethod
    def encode(image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
