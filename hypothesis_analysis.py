# hypothesis_analysis.py - version 1.1

from bloom_detection import detect_bloom_level

class HypothesisValidator:
    def __init__(self, doc, config, weights, bloom_verbs, bloom_synonyms, domain_lexicon=None):
        """
        doc            : spaCy Doc from hypothesis section
        config         : config_keywords.json
        weights        : weights for HYPOTHESIS in config_weights.json
        bloom_verbs    : diccionary of BLOOM_VERBS
        bloom_synonyms : diccionary of BLOOM_SYNONYMS
        domain_lexicon : dict with words sets for POS y 'ALL', o None
                         p.ej. {"NOUN": set(...), "VERB": set(...), "ADJ": set(...), "ALL": set(...)}
        """
        self.doc = doc
        self.config = config
        self.weights = weights
        self.bloom_verbs = bloom_verbs
        self.bloom_synonyms = bloom_synonyms
        self.domain_lexicon = domain_lexicon
        self.feedback = []
        self.score = 0

    def validate(self):
        total = sum(self.weights.values()) if self.weights else 1
        text_lower = self.doc.text.lower()
        lemmas_lower = [t.lemma_.lower() for t in self.doc]

        # 1) Tone
        tone_flag = any(phrase.lower() in text_lower for phrase in self.config.get("HYPOTHESIS_TONE_PHRASES", []))
        if tone_flag:
            self.feedback.append(f"Hypothesis uses appropriate scientific tone (+{self.weights.get('tone', 0)})")
            self.score += self.weights.get("tone", 0)
        else:
            self.feedback.append("Hypothesis tone may be too weak or informal (+0)")

        # 2) Relation/causality
        relation_flag = any(token_lemma in self.config.get("CAUSAL_VERBS", []) for token_lemma in lemmas_lower)
        if relation_flag:
            self.feedback.append(f"Relationship between variables is stated (+{self.weights.get('relation', 0)})")
            self.score += self.weights.get("relation", 0)
        else:
            self.feedback.append("Relationship between variables is not clearly expressed (+0)")

        # 3) Domain specificity: DOMAIN_KEYWORDS + curated lexicon
        domain_weight = self.weights.get("domain", 0)

        # a) Matches with DOMAIN_KEYWORDS from JSON
        domain_keywords = [kw.lower() for kw in self.config.get("DOMAIN_KEYWORDS", [])]
        hits_config = {lemma for lemma in lemmas_lower if lemma in domain_keywords}

        # b) Matches with the domain lexicon, if one exists
        hits_lexicon = set()
        if self.domain_lexicon is not None:
            lex_all = self.domain_lexicon.get("ALL", set())
            hits_lexicon = {lemma for lemma in lemmas_lower if lemma in lex_all}

        # c) Both sources of evidence
        combined_hits = hits_config | hits_lexicon
        domain_flag = bool(combined_hits) and domain_weight > 0

        if domain_weight > 0:
            if combined_hits:
                sample = ", ".join(sorted(list(combined_hits))[:5])
                self.feedback.append(
                    f"Hypothesis content is domain-specific ({len(combined_hits)} terms; e.g., {sample}) "
                    f"(+{domain_weight})"
                )
                self.score += domain_weight
            else:
                self.feedback.append("Hypothesis may lack scientific specificity (+0)")

        # 4) Bloom level
        bloom_msg, bloom_factor = detect_bloom_level(self.doc, self.bloom_verbs, self.bloom_synonyms)
        self.feedback.append(bloom_msg)
        self.score += self.weights.get("bloom", 0) * bloom_factor
        bloom_flag = bloom_factor > 0

        # 5) Contextual hypothesis summary
        self.feedback.append("\n[Contextual Hypothesis Summary]")

        # Good dominio, but no clear relationship
        if domain_flag and not relation_flag:
            self.feedback.append(
                "The hypothesis uses domain-specific terminology, "
                "but the relationship betweenthe main variables is not clearly expressed. "
                "Consider stating explicitly how the intervention, mechanism or pathway is expected to influence the outcome."
            )

        # Good domain, but no high level in Bloom verbs
        if domain_flag and not bloom_flag:
            self.feedback.append(
                "The hypothesis is scientifically specific, "
                "but does not use strong action verbs at higher Bloom levels. "
                "Consider reformulating the hypothesis using such verbs."
            )

        # Relationship or connections, but the tone is weak
        if relation_flag and not tone_flag:
            self.feedback.append(
                "The causal or correlative relationship is present, "
                "but the hypothesis tone may sound weak or informal. "
                "Consider using more explicit hypothesis markers."
            )

        # No tone, relationship, dominance, or Bloom
        if not (tone_flag or relation_flag or domain_flag or bloom_flag):
            self.feedback.append(
                "The current hypothesis formulation appears too generic. Consider: "
                "1) using explicit hypothesis phrases (e.g., 'We hypothesize that...'), "
                "2) expressing the relationship between variables clearly, "
                "3) including domain-specific terms, and "
                "4) adding higher-level action verbs aligned with Bloom's taxonomy."
            )

        percentage = (self.score / total) * 100
        return self.feedback, round(percentage, 1)
