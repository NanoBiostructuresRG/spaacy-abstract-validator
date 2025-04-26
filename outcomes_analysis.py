# outcomes_analysis.py - OOP version

from bloom_detection import detect_bloom_level

class OutcomesValidator:
    def __init__(self, doc, bloom_verbs, bloom_synonyms, weights):
        self.doc = doc
        self.bloom_verbs = bloom_verbs
        self.bloom_synonyms = bloom_synonyms
        self.weights = weights
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values())

        text_lower = self.doc.text.lower()

        has_direct_tone = any(phrase in text_lower for phrase in [
            "is expected to", "aims to", "is anticipated to"])

        has_future = any(tok.tag_ in ["MD", "VB"] and tok.text.lower() == "will" for tok in self.doc)

        self.feedback.append(
            f"Uses direct and impersonal scientific tone (+{self.weights['tone']})"
            if has_direct_tone else
            "Tone may be too speculative or weak (+0)"
        )
        self.score += self.weights["tone"] if has_direct_tone else 0

        self.feedback.append(
            f"Future-oriented verbs detected (+{self.weights['future']})"
            if has_future else
            "No future projection detected (+0)"
        )
        self.score += self.weights["future"] if has_future else 0

        bloom_msg, bloom_factor = detect_bloom_level(self.doc, self.bloom_verbs, self.bloom_synonyms)
        self.feedback.append(bloom_msg)
        self.score += self.weights["bloom"] * bloom_factor

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
