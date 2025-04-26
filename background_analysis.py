# background_analysis.py - OOP version

class BackgroundValidator:
    def __init__(self, doc, config, weights):
        self.doc = doc
        self.config = config
        self.weights = weights
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values())

        if any(token.lemma_ in self.config["PROBLEM_KEYWORDS"] for token in self.doc):
            self.feedback.append(f"Problem statement detected (+{self.weights['problem']})")
            self.score += self.weights["problem"]
        else:
            self.feedback.append("No clear problem statement found (+0)")

        if any(token.lemma_ in self.config["JUSTIFICATION_KEYWORDS"] for token in self.doc):
            self.feedback.append(f"Contextual justification detected (+{self.weights['justification']})")
            self.score += self.weights["justification"]
        else:
            self.feedback.append("No justification or context provided (+0)")

        if any(keyword.lower() in self.doc.text.lower() for keyword in self.config["CONCEPT_KEYWORDS"]):
            self.feedback.append(f"Key concept introduced (+{self.weights['concept']})")
            self.score += self.weights["concept"]
        else:
            self.feedback.append("No core concept or approach introduced (+0)")

        if any(phrase in self.doc.text.lower() for phrase in self.config["KNOWLEDGE_GAP_PHRASES"]):
            self.feedback.append(f"Knowledge gap clearly identified (+{self.weights['knowledge_gap']})")
            self.score += self.weights["knowledge_gap"]
        else:
            self.feedback.append("No explicit knowledge gap identified (+0)")

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
