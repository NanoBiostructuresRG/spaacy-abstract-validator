# abstract_validator.py - OOP version of the Abstract Validator

import spacy
import datetime
import os
import re
from config import INPUT_FILE, CONFIG_FILE, WEIGHT_FILE, OUTPUT_FILE
from loader import Loader
from background_analysis import BackgroundValidator
from hypothesis_analysis import HypothesisValidator
from methodology_analysis import MethodologyValidator
from outcomes_analysis import OutcomesValidator
from impact_analysis import ImpactValidator
from ethics_analysis import EthicsValidator
from summarizer import Summarizer


class AbstractValidator:
    def __init__(self, input_file, config_file, weight_file, output_file):
        self.loader = Loader(input_file, config_file, weight_file)
        self.output_file = output_file
        self.nlp = spacy.load("en_core_web_sm")
        self.results = []
        self.keywords = []

    def load_resources(self):
        self.config = self.loader.load_config()
        self.weights = self.loader.load_weights()
        raw_text = self.loader.load_text()
        background, hypothesis, methodology, outcomes, impact, keywords = self.loader.split_sections(raw_text)
        self.keywords = keywords
        self.background_doc = self.nlp(background)
        self.hypothesis_doc = self.nlp(hypothesis)
        self.methodology_doc = self.nlp(methodology)
        self.outcomes_doc = self.nlp(outcomes)
        self.impact_doc = self.nlp(impact)
        self.sections = [background, hypothesis, methodology, outcomes, impact]
        
    def process_sections(self):
        (self.background_doc,
         self.hypothesis_doc,
         self.methodology_doc,
         self.outcomes_doc,
         self.impact_doc) = [self.nlp(section) for section in self.sections]

    def add_header(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = [
            "==================================================",
            "       SCIENTIFIC PROPOSAL ABSTRACT ANALIZER",
            "        Natural Language Processing (SpaCy)",
            "--------------------------------------------------",
            "Developer: Flavio F. Contreras-Torres",
            "Version: v.1.0 - Oviedo",
            f"Execution Date: {now}",
            "--------------------------------------------------",
            "GitHub: https://github.com/NanoBiostructuresRG",
            "==================================================\n"
        ]
        self.results.extend(header)

    def validate_background(self):
        validator = BackgroundValidator(self.background_doc, self.config, self.weights["BACKGROUND"])
        feedback, score = validator.validate()
        self.results.append("[1. BACKGROUND VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nBKG_SCORE: {score}%\n")

    def validate_hypothesis(self):
        validator = HypothesisValidator(
            self.hypothesis_doc,
            self.config,
            self.weights["HYPOTHESIS"],
            self.config["BLOOM_VERBS"],
            self.config["BLOOM_SYNONYMS"]
        )
        feedback, score = validator.validate()
        self.results.append("\n[2. HYPOTHESIS VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nHYP_SCORE: {score}%\n")

    def validate_methodology(self):
        validator = MethodologyValidator(
            self.methodology_doc,
            self.config["BLOOM_VERBS"],
            self.config["BLOOM_SYNONYMS"],
            self.weights["METHODOLOGY"]
        )
        feedback, score = validator.validate()
        self.results.append("\n[3. METHODOLOGY VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nMETH_SCORE: {score}%\n")

    def validate_outcomes(self):
        validator = OutcomesValidator(
            self.outcomes_doc,
            self.config["BLOOM_VERBS"],
            self.config["BLOOM_SYNONYMS"],
            self.weights["OUTCOMES"]
        )
        feedback, score = validator.validate()
        self.results.append("\n[4. EXPECTED OUTCOMES VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nOUT_SCORE: {score}%\n")

    def validate_impact(self):
        validator = ImpactValidator(
            self.impact_doc,
            self.config["BLOOM_VERBS"],
            self.config["BLOOM_SYNONYMS"],
            self.weights["IMPACT"]
        )
        feedback, score = validator.validate()
        self.results.append("\n[5. IMPACT VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nIMPACT_SCORE: {score}%\n")

    def validate_ethics(self):
        validator = EthicsValidator(
            self.impact_doc,
            self.config["ETHICS_KEYWORDS"],
            self.weights["ETHICS"]
        )
        feedback, score = validator.validate()
        self.results.append("\n[6. ETHICS VALIDATION]\n")
        self.results.extend(feedback)
        self.results.append(f"\nETHICS_SCORE: {score}%\n")

    def summarize_abstract(self):
        full_text = " ".join(self.sections)
        full_doc = self.nlp(full_text)
        if self.keywords:
            full_text_lower = full_text.lower()
            
        matched_keywords = []
        for kw in self.keywords:
            if kw.lower() in full_text_lower:
                matched_keywords.append(kw)
        if matched_keywords:
            print(f"Keywords matched: {len(matched_keywords)} of {len(self.keywords)}")
        else:
            print(f"Warning: No keywords were detected in the abstract. Summary generated without keyword influence.")
       
        summarizer = Summarizer(full_doc, keywords=self.keywords)
        summary = summarizer.summarize()
        self.results.append("\n[7. ABSTRACT SUMMARY]\n")
        self.results.append(summary)

    def save_results(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.results))
        print(f"Validation completed. Results saved to: {self.output_file}")
    
    def save_results(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.results))
        print(f"Validation completed. Results saved to: {self.output_file}")

    def run(self):
        self.load_resources()
        self.process_sections()
        self.add_header()
        self.validate_background()
        self.validate_hypothesis()
        self.validate_methodology()
        self.validate_outcomes()
        self.validate_impact()
        self.validate_ethics()
        self.summarize_abstract()
        self.save_results()


if __name__ == "__main__":
    validator = AbstractValidator(INPUT_FILE, CONFIG_FILE, WEIGHT_FILE, OUTPUT_FILE)
    validator.run()
