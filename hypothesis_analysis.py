# hypothesis_analysis.py - OOP version

from bloom_detection import detect_bloom_level

class HypothesisValidator:
    def __init__(self, doc, config, weights, bloom_verbs, bloom_synonyms):
        self.doc = doc
        self.config = config
        self.weights = weights
        self.bloom_verbs = bloom_verbs
        self.bloom_synonyms = bloom_synonyms
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values())

        if any(phrase in self.doc.text.lower() for phrase in self.config["HYPOTHESIS_TONE_PHRASES"]):
            self.feedback.append(f"Hypothesis uses appropriate scientific tone (+{self.weights['tone']})")
            self.score += self.weights["tone"]
        else:
            self.feedback.append("Hypothesis tone may be too weak or informal (+0)")

        if any(token.lemma_.lower() in self.config["CAUSAL_VERBS"] for token in self.doc):
            self.feedback.append(f"Relationship between variables is stated (+{self.weights['relation']})")
            self.score += self.weights["relation"]
        else:
            self.feedback.append("Relationship between variables is not clearly expressed (+0)")

        if any(token.lemma_.lower() in self.config["DOMAIN_KEYWORDS"] for token in self.doc):
            self.feedback.append(f"Hypothesis content is relevant and specific (+{self.weights['domain']})")
            self.score += self.weights["domain"]
        else:
            self.feedback.append("Hypothesis may lack scientific specificity (+0)")

        bloom_msg, bloom_factor = detect_bloom_level(self.doc, self.bloom_verbs, self.bloom_synonyms)
        self.feedback.append(bloom_msg)
        self.score += self.weights["bloom"] * bloom_factor

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
