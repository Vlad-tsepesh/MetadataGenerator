from openai import OpenAI
import json


class MetadataGenerator:
    def __init__(self, client: OpenAI, prompt: str):
        self.client = client
        self.prompt = prompt

    def generate(self, base64_image: str) -> dict:
        response = self.client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": self.prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        return json.loads(response.output_text)