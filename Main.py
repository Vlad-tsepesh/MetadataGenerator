from openai import OpenAI

from batch_processor import BatchProcessor
from image_encoder import ImageEncoder
from image_metadata_writer import ImageMetadataWriter
from metadata_generator import MetadataGenerator

if __name__ == "__main__":
    PROMPT = """..."""
    client = OpenAI()

    encoder = ImageEncoder()
    generator = MetadataGenerator(client, PROMPT)
    writer = ImageMetadataWriter()

    processor = BatchProcessor("D:\\projects\\images", encoder, generator, writer)
    processor.process()