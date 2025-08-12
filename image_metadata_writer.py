import os

import piexif
from PIL import Image


class ImageMetadataWriter:
    @staticmethod
    def to_utf16le_bytes(text: str) -> bytes:
        return text.encode("utf-16le") + b"\x00\x00"

    def write_metadata(self, image_path: str, title: str, description: str, keywords: str, output_path: str):
        image = Image.open(image_path)
        exif_bytes = image.info.get("exif")
        exif_dict = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {},
                                                                "thumbnail": None}

        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")
        exif_dict["0th"][piexif.ImageIFD.XPTitle] = self.to_utf16le_bytes(title)
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = self.to_utf16le_bytes(keywords)

        exif_bytes = piexif.dump(exif_dict)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, exif=exif_bytes)
