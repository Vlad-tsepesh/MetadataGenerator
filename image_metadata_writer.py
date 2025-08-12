import os
from iptcinfo3 import IPTCInfo

class ImageMetadataWriter:
    def write_metadata(self, image_path, title, description, keywords, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        info = IPTCInfo(image_path, force=True)
        info['object name'] = title
        info['caption/abstract'] = description
        info['keywords'] = [kw.strip() for kw in keywords.split(",")]
        info.save_as(output_path)
