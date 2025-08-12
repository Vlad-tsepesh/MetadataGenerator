import os

from image_encoder import ImageEncoder


class BatchProcessor:
    def __init__(self, folder_path: str, encoder: ImageEncoder, generator: MetadataGenerator,
                 writer: ImageMetadataWriter):
        self.folder_path = folder_path
        self.encoder = encoder
        self.generator = generator
        self.writer = writer

    def process(self):
        supported_ext = {".jpg", ".jpeg", ".png"}
        for filename in os.listdir(self.folder_path):
            if os.path.splitext(filename.lower())[1] in supported_ext:
                file_path = os.path.join(self.folder_path, filename)
                try:
                    print(f"Processing {file_path} ...")
                    base64_image = self.encoder.encode(file_path)
                    metadata = self.generator.generate(base64_image)
                    output_dir = os.path.join(self.folder_path, "..", "images_with_metadata")
                    output_path = os.path.join(output_dir, filename)
                    self.writer.write_metadata(file_path, metadata['title'], metadata['description'],
                                               metadata['keywords'], output_path)
                    print(f"Saved with metadata: {output_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
