import base64
import json
from openai import OpenAI

import piexif
from PIL import Image


client = OpenAI()

PROMPT = """
Generates professional stock descriptions for Adobe Stock, with titles, descriptions, and keywords.
Instructions: This GPT will provide professional image descriptions for stock image submissions to Adobe Stock. It will generate concise, clear titles, descriptions, and keywords in English, aimed at selling the images effectively on stock websites. The title should be between 1 to 7 words, the description should be no longer than 200 characters, and the keywords should be between 20 and 48, separated by commas. The descriptions will follow best practices used by top stock contributors, emphasizing relevance, color, composition, and potential commercial usage. It will focus on universal appeal and visual storytelling, avoiding overuse of technical terms or subjective interpretations. The goal is to describe the image in a way that appeals to both creative professionals and commercial buyers, ensuring wide usability. Keywords will be carefully chosen to maximize visibility in search results and cover various use cases for the image. The tone will be professional but approachable, guiding the user smoothly through each step of the process.
Output: Output should be a JSON with (title, description, keywords) as a key and the result of the prompt for the specific key as a value.
"""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "bike.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": PROMPT},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)
metadata = json.loads(response.output_text)


def to_utf16le_bytes(text):
    # Convert Python str to UTF-16LE encoded bytes with a null terminator
    return text.encode('utf-16le') + b'\x00\x00'

# Your metadata (example)
title = metadata['title']
description = metadata['description']
keywords = metadata['keywords']  # comma-separated string

# Load the image
image = Image.open(image_path)

# Load existing EXIF data or initialize new

exif_bytes = image.info.get("exif")

if exif_bytes:
    exif_dict = piexif.load(exif_bytes)
else:
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

# Set ImageDescription (0th IFD) - good for description or title
exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode('utf-8')

# Set XPTitle (0th IFD) - Windows specific title tag
exif_dict["0th"][piexif.ImageIFD.XPTitle] = to_utf16le_bytes(title)

# Set XPKeywords (0th IFD) - keywords list as UTF-16LE
exif_dict["0th"][piexif.ImageIFD.XPKeywords] = to_utf16le_bytes(keywords)

# Dump EXIF bytes
exif_bytes = piexif.dump(exif_dict)

# Save image with new EXIF metadata (overwrite original or new file)
image.save("bike_with_metadata.jpg", exif=exif_bytes)
