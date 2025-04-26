# ethics_analysis.py - OOP version

class EthicsValidator:
    def __init__(self, doc, keywords, weights):
        self.doc = doc
        self.keywords = keywords
        self.weights = weights
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values())
        text_lower = self.doc.text.lower()

        ethics_mentioned = any(phrase in text_lower for phrase in self.keywords)

        if ethics_mentioned:
            self.feedback.append(f"Ethical approval or considerations detected (+{self.weights['mention']})")
            self.score += self.weights["mention"]
        else:
            self.feedback.append("No explicit mention of ethical approval or considerations (+0)")

        percentage = (self.score / total) * 100 if total > 0 else 0
        return self.feedback, round(percentage, 1)
