import argparse

class ArgumentParserService:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Process images and add metadata.")
        self.parser.add_argument("path", help="Path to an image or folder")

    def parse(self):
        return self.parser.parse_args()
