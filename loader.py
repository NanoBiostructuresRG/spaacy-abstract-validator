# loader.py - OOP version

import json

class Loader:
    def __init__(self, input_file, config_file, weight_file):
        self.input_file = input_file
        self.config_file = config_file
        self.weight_file = weight_file

    def load_text(self):
        with open(self.input_file, "r", encoding="utf-8") as f:
            return f.read()

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_weights(self):
        with open(self.weight_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def split_sections(self, text):
        sections = text.split("#")[1:]  # Skip anything before the first #
        sections = [s.strip() for s in sections]
        background, hypothesis, methodology, outcomes, impact, keywords = [""] * 6
        for sec in sections:
            if sec.lower().startswith("background"):
                background = sec[len("background"):].strip()
            elif sec.lower().startswith("hypothesis"):
                hypothesis = sec[len("hypothesis"):].strip()
            elif sec.lower().startswith("methodology"):
                methodology = sec[len("methodology"):].strip()
            elif sec.lower().startswith("outcomes"):
                outcomes = sec[len("outcomes"):].strip()
            elif sec.lower().startswith("impact"):
                impact = sec[len("impact"):].strip()
            elif sec.lower().startswith("keywords"):
                keywords = [kw.strip() for kw in sec[len("keywords"):].strip().split(",") if kw.strip()]
        return background, hypothesis, methodology, outcomes, impact, keywords
