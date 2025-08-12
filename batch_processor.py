import os

from image_encoder import ImageEncoder
from image_metadata_writer import ImageMetadataWriter
from metadata_generator import MetadataGenerator


class BatchProcessor:
    def __init__(self, path: str, encoder: ImageEncoder, generator: MetadataGenerator,
                 writer: ImageMetadataWriter):
        self.path = path
        self.encoder = encoder
        self.generator = generator
        self.writer = writer
        self.supported_ext = {".jpg", ".jpeg", ".png"}
        self.files = None

    def process_path(self):
        if os.path.isdir(self.path):
            self.files = [os.path.join(self.path, f) for f in os.listdir(self.path)]
        elif os.path.isfile(self.path):
            self.files = [self.path]
        else:
            print(f"Invalid path: {self.path}")
            return

    def _is_supported(self, file_path):
        extension = os.path.splitext(file_path.lower())[1]
        return extension in self.supported_ext

    def _process_file(self):
        for file_path in self.files:
            if self._is_supported(file_path):

                try:
                    print(f"Processing {file_path} ...")
                    base64_image = self.encoder.encode(file_path)
                    metadata = self.generator.generate(base64_image)
                    extension = os.path.splitext(file_path.lower())[1]
                    output_dir = os.path.join(os.path.dirname(file_path), "..", "images_with_metadata")
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, f"{metadata['title']}{extension}")
                    self.writer.write_metadata(
                        file_path,
                        metadata['title'],
                        metadata['description'],
                        metadata['keywords'],
                        output_path
                    )
                    print(f"Saved with metadata: {output_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    def process(self):
        self.process_path()
        self._process_file()
