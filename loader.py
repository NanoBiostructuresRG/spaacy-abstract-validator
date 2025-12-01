# loader.py - version 1.1

import json
import os
import pandas as pd

class Loader:
    def __init__(self,
        input_file: str,
        config_file: str,
        weight_file: str,
        lexicon_dir: str = "lexicon",
        domain_tag: str | None = None,
    ):
        """
        input_file   : path to the abstract text file
        config_file  : path to config_keywords.json
        weight_file  : path to config_weights.json
        lexicon_dir  : base directory for domain lexicons (default: 'lexicon')
        domain_tag   : optional domain/tag to load a curated lexicon (e.g., 'pparg')
        """
        self.input_file = input_file
        self.config_file = config_file
        self.weight_file = weight_file
        self.lexicon_dir = lexicon_dir
        self.domain_tag = domain_tag  # e.g. 'pparg', 'cb1', 'obesity'

    # ----------------------------
    # Existing methods 
    # ----------------------------
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

    # ----------------------------
    # Domain lexicon support
    # ----------------------------
    def load_domain_lexicon(self, tag: str | None = None):
        """
        Load a curated lexicon for a given domain/tag from:
            lexicon/<tag>/lexicon_<tag>.csv

        Returns:
            dict with sets of words per POS:
                {
                    "NOUN": set(...),
                    "VERB": set(...),
                    "ADJ":  set(...),
                    "ALL":  set(...)
                }
            or None if no tag or file not found.
        """
        tag = tag or self.domain_tag
        if tag is None:
            return None

        tag_norm = tag.lower()
        csv_path = os.path.join(self.lexicon_dir, tag_norm, f"lexicon_{tag_norm}.csv")

        if not os.path.exists(csv_path):
            print(f"[WARN] Domain lexicon not found for tag '{tag}': {csv_path}")
            return None

        df = pd.read_csv(csv_path)

        expected_cols = {"word", "pos", "frequency"}
        if not expected_cols.issubset(df.columns):
            print(f"[WARN] Invalid lexicon schema in {csv_path}. Expected columns: {expected_cols}")
            return None

        # Normalize words to lowercase strings
        df["word"] = df["word"].astype(str).str.lower()

        lexicon = {
            "NOUN": set(df.loc[df["pos"] == "NOUN", "word"]),
            "VERB": set(df.loc[df["pos"] == "VERB", "word"]),
            "ADJ":  set(df.loc[df["pos"] == "ADJ",  "word"]),
            "ALL":  set(df["word"])
        }
        return lexicon

    def load_all(self):
        """
        Convenience method:
        Returns a tuple: (text, config_keywords, config_weights, domain_lexicon)
        """
        text = self.load_text()
        config_keywords = self.load_config()
        config_weights = self.load_weights()
        domain_lexicon = self.load_domain_lexicon()
        return text, config_keywords, config_weights, domain_lexicon