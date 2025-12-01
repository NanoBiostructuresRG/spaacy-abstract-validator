# SPAA: Scientific Proposal Abstract Analyzer
**Version 1.1.0 - November, 2025. Monterrey**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Version](https://img.shields.io/badge/version-v1.1-blue.svg)]()

---

## Description
**SPAA** is an automated evaluator of scientific abstracts that integrates narrative/ rhetorical analysis with domain-dependent scientific–technical verification. It applies linguistic, semantic, and structural rules—together with curated domain-specific lexicons—to assess the quality of the background, hypothesis, methodology, expected outcomes, and impact sections. Using NLP (SpaCy), SPAA generates a report with expert-level feedback on the abstract’s coherence, rigor, and scientific soundness.

---

## Purpose
**SPAA** evaluates whether a research abstract:
- States a clear problem, context, and knowledge gap.
- Formulates a specific and domain-relevant hypothesis.
- Describes a coherent methodological plan.
- Defines expected outcomes aligned with the study goals.
- Identifies scientific or societal impact.
- Uses domain-appropriate terminology based on curated lexicons.
- Employs proper academic tone, causal structure, and strong action verbs.
- Produces a consistent, reproducible evaluation report.
- Generates a concise abstract summary based on keyword relevance.

---

## Project Structure
```text
SPAA/
├── abstract_validator.py               # Orchestrates the validation pipeline (main OOP engine)
├── loader.py                           # Class to load input text and configuration files
├── background_analysis.py              # Background section validator
├── hypothesis_analysis.py              # Hypothesis section validator
├── methodology_analysis.py             # Methodology section validator
├── outcomes_analysis.py                # Expected Outcomes section validator
├── impact_analysis.py                  # Impact section validator
├── ethics_analysis.py                  # Ethics validator
├── summarizer.py                       # Summarizes the abstract automatically
├── bloom_detection.py                  # Bloom's Taxonomy detection utilities
├── lexicon/
│   ├── <tag_1>/lexicon_<tag_1>.csv     # Lexicon list for <tag_1>
│   ├── <tag_2>/lexicon_<tag_2>.csv     # Lexicon list for <tag_2>
│   └── <tag_N>/lexicon_<tag_N>.csv     # Lexicon list for <tag_N>
├── config/
│   ├── config_keywords.json            # Keyword lists and synonyms
│   └── config_weights.json             # Scoring weights per section
├── input_data/
│   └── abstract_file.txt               # Abstract to be evaluated (structured with # sections)
├── output/
│   └── output_results.txt              # Generated validation report
└── README.md   
```

---

## Dependencies
- Python 3.10
- SpaCy

Install dependencies with:
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

---

## How to Run
From the root folder:
```bash
python abstract_validator.py
```

Make sure your input file (`abstract_file.txt`) inside `input_data/` follows this format:
```
# background
[Text about the background]

# hypothesis
[Text about the hypothesis]

# methodology
[Text about the planned methods]

# outcomes
[Text about the expected outcomes]

# impact
[Text about the long-term impact]

# keywords
keyword1, keyword2, keyword3, ..., keyword5
```

---

## Output
A console message and a saved file under `output/`, containing:
- Validation feedback section by section
- Scores (%) for each evaluated part
- Detection of strong/weak scientific tone
- Detection of Bloom's action verbs (and their level)

Example console output:
```
Keywords matched: 3 of 5
Validation completed. Results saved to: output/output_results.txt
```

---

## Notes
- All keyword rules and scoring weights can be customized via JSON files (`config/` folder).
- Bloom verb detection includes synonyms to ensure broader linguistic coverage.
- Designed for scientific proposal abstracts, not intended for finalized manuscripts.

---

## Future Extensions
- Domain taxonomies: High-level ontologies  to classify concepts and detect topic alignment.
- Multi-domain lexicon fusion: Combine lexicons for cross-disciplinary abstracts.
- Extending to multi-language support (e.g., Spanish abstract).

---

## Author
Developed by **Flavio F. Contreras-Torres** (Tecnológico de Monterrey)
Monterrey, Mexico - November 2025

---

## Versions
v.1.0.0 - April 2025. Oviedo, Spain
v.1.1.0 - November 2025. Monterrey, Mexico

---

## License
This project is licensed under the terms of the [MIT License](https://github.com/NanoBiostructuresRG/spaacy-abstract-validator/blob/main/LICENSE).  
See the LICENSE file for full details.