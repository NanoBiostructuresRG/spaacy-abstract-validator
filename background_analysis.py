# background_analysis.py - version 1.1

class BackgroundValidator:
    def __init__(self, doc, config, weights, domain_lexicon=None):
        """
        doc            : spaCy Doc from background section
        config         : diccionary from config_keywords.json
        weights        : diccionary of weights for BACKGROUND (config_weights.json)
                         p.ej. {"problem": 25, "justification": 25, "concept": 25, "knowledge_gap": 25, "domain": 20}
        domain_lexicon : dict with words sets for POS y 'ALL', o None
                         p.ej. {"NOUN": set(...), "VERB": set(...), "ADJ": set(...), "ALL": set(...)}
        """
        self.doc = doc
        self.config = config
        self.weights = weights
        self.domain_lexicon = domain_lexicon
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values()) if self.weights else 1
        text_lower = self.doc.text.lower()
        lemmas_lower = [t.lemma_.lower() for t in self.doc]

        # 1) Problem
        problem_flag = any(kw.lower() in lemmas_lower for kw in self.config.get("PROBLEM_KEYWORDS", []))
        
        if problem_flag:
            self.feedback.append(f"Problem statement detected (+{self.weights.get('problem', 0)})")
            self.score += self.weights.get("problem", 0)
        else:
            self.feedback.append("No clear problem statement found (+0)")

        # 2) Justification / context
        justification_flag = any(kw.lower() in lemmas_lower for kw in self.config.get("JUSTIFICATION_KEYWORDS", []))
        
        if justification_flag: 
            self.feedback.append(f"Contextual justification detected (+{self.weights.get('justification', 0)})")
            self.score += self.weights.get("justification", 0)
        else:
            self.feedback.append("No justification or contextal frame provided (+0)")

        # 3) Key concepto / approach
        concept_flag = any(keyword.lower() in text_lower for keyword in self.config.get("CONCEPT_KEYWORDS", []))
        
        if concept_flag:
            self.feedback.append(f"Key concept introduced (+{self.weights.get('concept', 0)})")
            self.score += self.weights.get("concept", 0)
        else:
            self.feedback.append("No core scientific concept or approach introduced (+0)")

        # 4) Knowledge gap
        gap_flag = any(phrase.lower() in text_lower for phrase in self.config.get("KNOWLEDGE_GAP_PHRASES", []))
        
        if gap_flag:
            self.feedback.append(f"Knowledge gap clearly identified (+{self.weights.get('knowledge_gap', 0)})")
            self.score += self.weights.get("knowledge_gap", 0)
        else:
            self.feedback.append("No explicit knowledge gap identified (+0)")

        # 5) Domain lexicon
        domain_weight = self.weights.get("domain", 0)
        domain_hits = set()

        if self.domain_lexicon is not None and domain_weight > 0:
            # Intersection between background and lexicon lemmas["ALL"]
            lex_all = self.domain_lexicon.get("ALL", set())
            domain_hits = {lemma for lemma in lemmas_lower if lemma in lex_all}

            if domain_hits:
                sample = ", ".join(sorted(list(domain_hits))[:5])
                self.feedback.append(
                    f"Domain-specific terminology detected ({len(domain_hits)} terms; e.g., {sample}) "
                    f"(+{domain_weight})"
                )
                self.score += domain_weight
            else:
                self.feedback.append(
                    "Background lacks domain-specific terminology from the curated lexicon (+0)"
                )
        
        # 6) Contextual summary
        self.feedback.append("\n[Contextual Background Summary]")

        # Domain dominance, but no gap
        if domain_hits and not gap_flag:
            self.feedback.append(
                "The background demonstrates strong familiarity with the scientific domain, "
                "but does not articulate what is unknown or insufficiently understood. "
                "Consider explicitly stating the knowledge gap to justify the study."
            )

        # Domain dominance, but no problem statement
        if domain_hits and not problem_flag:
            self.feedback.append(
                "The background demonstrates strong familiarity with the scientific domain, "
                "but the specific problem is not clearly formulated. "
                "Adding a concise problem statement will improve clarity and motivation."
            )

        # Problem statement, but no justification
        if problem_flag and not justification_flag:
            self.feedback.append(
                "The problem is mentioned, "
                "but its broader relevance is not fully justified. "
                "Explain why this issue matters (clinical, technological, or societal impact)."
            )

        # There is a gap, but with almost no domain terminology
        if gap_flag and not domain_hits:
            self.feedback.append(
                "A knowledge gap is stated, "
                "but the background lacks domain-specific details. "
                "Consider incorporating more contextual terminology to anchor the gap in a clear scientific scenario."
            )

        # Everything is very sluggish
        if not (problem_flag or justification_flag or concept_flag or gap_flag):
            self.feedback.append(
                "The background remains very generic. Consider explicitly adding: "
                "1) a clear problem, " 
                "2) a justification or context, "
                "3) at least one core concept, and "
                "4) The specific knowledge gap."
            )

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
