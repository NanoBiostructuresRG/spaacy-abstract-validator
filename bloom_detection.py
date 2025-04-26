# bloom_detection.py - (differentiated scoring)

def detect_bloom_level(doc, bloom_verbs, bloom_synonyms):
    found_exact = set()
    found_synonym = set()

    for token in doc:
        if token.pos_ == "VERB":
            lemma = token.lemma_.lower()
            # Direct match in BLOOM_VERBS
            for level, verbs in bloom_verbs.items():
                if lemma in verbs:
                    found_exact.add(level)
            # Indirect match in BLOOM_SYNONYMS
            for core, synonyms in bloom_synonyms.items():
                if lemma in synonyms:
                    # Need to find what Bloom level the core belongs to
                    for level, verbs in bloom_verbs.items():
                        if core in verbs:
                            found_synonym.add(level)

    # Priority: HIGH > MEDIUM > LOW
    if "HIGH" in found_exact:
        return ("Bloom level: HIGH (exact match)", 1.0)
    elif "HIGH" in found_synonym:
        return ("Bloom level: HIGH (via synonym)", 0.8)
    elif "MEDIUM" in found_exact:
        return ("Bloom level: MEDIUM (exact match)", 0.7)
    elif "MEDIUM" in found_synonym:
        return ("Bloom level: MEDIUM (via synonym)", 0.6)
    elif "LOW" in found_exact:
        return ("Bloom level: LOW (exact match)", 0.4)
    elif "LOW" in found_synonym:
        return ("Bloom level: LOW (via synonym)", 0.3)
    else:
        return ("No Bloom-level verbs detected.", 0.0)
