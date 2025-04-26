# Abstract Validator - Scientific Proposal Analyzer (OOP Edition)
Version 1.0.0 - Oviedo

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Description
This tool automatically validates scientific proposal abstracts, analyzing their structure and language section by section.
Now redesigned using a fully object-oriented architecture (OOP) for greater clarity, maintainability, and scalability.

## Purpose
Automatically evaluate whether an abstract:
- Clearly presents a scientific problem and concept.
- States a sound and specific hypothesis.
- Describes planned methodology appropriately.
- Projects meaningful expected outcomes.
- Anticipates relevant scientific or societal impact.
- Provides a concise and focused abstract summary using keyword-driven prioritization.

## Project Structure
```
abstract_validator/
├── abstract_validator.py       # Orchestrates the validation pipeline (main OOP engine)
├── loader.py                   # Class to load input text and configuration files
├── background_analysis.py      # Background section validator
├── hypothesis_analysis.py      # Hypothesis section validator
├── methodology_analysis.py     # Methodology section validator
├── outcomes_analysis.py        # Expected Outcomes section validator
├── impact_analysis.py          # Impact section validator
├── ethics_analysis.py          # Ethics validator
├── summarizer.py               # Summarizes the abstract automatically
├── bloom_detection.py          # Bloom's Taxonomy detection utilities
├── config/
│   ├── config_keywords.json    # Keyword lists and synonyms
│   └── config_weights.json     # Scoring weights per section
├── input_data/
│   └── abstract_file.txt       # Abstract to be evaluated (structured with # sections)
├── output/
│   └── output_results.txt      # Generated validation report
└── README.md   
```

## Dependencies
- Python 3.10
- SpaCy

Install dependencies with:
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

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

## Notes
- All keyword rules and scoring weights can be customized via JSON files (`config/` folder).
- Bloom verb detection includes synonyms to ensure broader linguistic coverage.
- Designed for scientific proposal abstracts, not intended for finalized manuscripts.

## Authors
Developed by Flavio F. Contreras-Torres (Tecnologico de Monterrey) for academic use and educational purposes.

## Future Extensions
- Adding new modules: literature review validation.
- Exporting results in JSON/HTML.
- Building a simple web app interface (Flask/FastAPI).
- Extending to multi-language suppoort (e.g., Spanish abstract).

