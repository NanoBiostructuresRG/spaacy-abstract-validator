# methodology_analysis.py - OOP version

from bloom_detection import detect_bloom_level

class MethodologyValidator:
    def __init__(self, doc, bloom_verbs, bloom_synonyms, weights):
        self.doc = doc
        self.bloom_verbs = bloom_verbs
        self.bloom_synonyms = bloom_synonyms
        self.weights = weights
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values())

        has_future = any(tok.tag_ in ["MD", "VB"] and tok.text.lower() == "will" for tok in self.doc)
        techniques = [tok.text for tok in self.doc if tok.pos_ == "NOUN" and tok.dep_ in ("nsubj", "dobj")]
        purpose_found = any(
            tok.lemma_.lower() in self.bloom_verbs["MEDIUM"] + self.bloom_verbs["HIGH"] or
            any(tok.lemma_.lower() in syns for syns in self.bloom_synonyms.values())
            for tok in self.doc if tok.pos_ == "VERB"
        )

        self.feedback.append("Future tense used to indicate planned actions." if has_future else "No future-oriented verbs found.")
        self.score += self.weights["future"] if has_future else 0

        self.feedback.append("Technical terms or methods mentioned." if techniques else "No methods or techniques detected.")
        self.score += self.weights["technique"] if techniques else 0

        self.feedback.append("Techniques are associated with analytical/evaluative purpose verbs." if purpose_found else "Techniques may lack clearly stated purpose.")
        self.score += self.weights["purpose"] if purpose_found else 0

        bloom_msg, bloom_factor = detect_bloom_level(self.doc, self.bloom_verbs, self.bloom_synonyms)
        self.feedback.append(bloom_msg)
        self.score += self.weights["bloom"] * bloom_factor

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
