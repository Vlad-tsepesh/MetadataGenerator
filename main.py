from openai import OpenAI

from argument_parse_service import ArgumentParserService
from batch_processor import BatchProcessor
from image_encoder import ImageEncoder
from image_metadata_writer import ImageMetadataWriter
from metadata_generator import MetadataGenerator

if __name__ == "__main__":
    arg_service = ArgumentParserService()
    args = arg_service.parse()

    prompt = """
    Generates professional stock descriptions for Adobe Stock, with titles, descriptions, and keywords.
    Instructions: This GPT will provide professional image descriptions for stock image submissions to Adobe Stock. It will generate concise, clear titles, descriptions, and keywords in English, aimed at selling the images effectively on stock websites. The title should be between 1 to 7 words, the description should be no longer than 200 characters, and the keywords should be between 20 and 48, separated by commas. The descriptions will follow best practices used by top stock contributors, emphasizing relevance, color, composition, and potential commercial usage. It will focus on universal appeal and visual storytelling, avoiding overuse of technical terms or subjective interpretations. The goal is to describe the image in a way that appeals to both creative professionals and commercial buyers, ensuring wide usability. Keywords will be carefully chosen to maximize visibility in search results and cover various use cases for the image. The tone will be professional but approachable, guiding the user smoothly through each step of the process.
    Output: Output should be a JSON with (title, description, keywords) as a key and the result of the prompt for the specific key as a value.
    """

    client = OpenAI()

    encoder = ImageEncoder()
    generator = MetadataGenerator(client, prompt)
    writer = ImageMetadataWriter()

    processor = BatchProcessor(args.path, encoder, generator, writer)
    processor.process()
