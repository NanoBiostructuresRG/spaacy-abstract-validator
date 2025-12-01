# summarizer.py version 1.1

class Summarizer:
    def __init__(self, doc, keywords=None, max_chars=2000):
        self.doc = doc
        self.keywords = [kw.lower() for kw in keywords] if keywords else []
        self.max_chars = max_chars
        self.sentences = [sent for sent in doc.sents]
        self.word_frequencies = {}
        self.sentence_scores = {}

    def calculate_frequencies(self):
        for token in self.doc:
            if token.is_stop == False and token.is_punct == False:
                word = token.text.lower()
                if word not in self.word_frequencies:
                    self.word_frequencies[word] = 1
                else:
                    self.word_frequencies[word] += 1

    def score_sentences(self):
        for sent in self.sentences:
            for word in sent:
                if word.text.lower() in self.word_frequencies:
                    if sent not in self.sentence_scores:
                        self.sentence_scores[sent] = self.word_frequencies[word.text.lower()]
                    else:
                        self.sentence_scores[sent] += self.word_frequencies[word.text.lower()]
        
            # Bonus if sentence contains a keyword
            sent_text = sent.text.lower()
            if any(kw in sent_text for kw in self.keywords):
                self.sentence_scores[sent] = self.sentence_scores.get(sent, 0) + 10  #bonus
                               
    def summarize(self, n_sentences=3):
        if not self.doc or not self.doc.text.strip():
            return ""
        
        self.calculate_frequencies()
        self.score_sentences()

        if not self.sentence_scores:
            return ""

        summarized = sorted(self.sentence_scores, key=self.sentence_scores.get, reverse=True)
        summarized = summarized[:n_sentences]
        summarized = sorted(summarized, key=lambda s: s.start)  # keep original order
        summary_text = " ".join([sent.text for sent in summarized])

        # Restricted up to max_chars (with spaces)
        if len(summary_text) > self.max_chars:
            cutoff_point = summary_text.rfind(" ", 0, self.max_chars)
            if cutoff_point == -1:
                cutoff_point = self.max_chars
            summary_text = summary_text[:cutoff_point].rstrip() + "..."

        return summary_text


class StructuredSummarizer:
    """
    Construye un resumen estructurado del abstract usando Summarizer sección por sección.
    """

    def __init__(self, keywords=None,
                 max_chars_per_section=400,
                 prefix_labels=True):
        """
        keywords              : lista de palabras clave del usuario (sección #keywords)
        max_chars_per_section : límite por defecto de caracteres para cada mini-resumen de sección
        prefix_labels         : si True, antepone 'Background:', 'Hypothesis:', etc.
        """
        self.keywords = [kw.lower() for kw in keywords] if keywords else []
        self.max_chars_per_section = max_chars_per_section
        self.prefix_labels = prefix_labels

    def _summarize_section(self, doc, n_sentences=1, max_chars_override=None):
        """
        Resumen extractivo de una sección individual.
        max_chars_override: si se pasa, domina sobre max_chars_per_section.
        """
        if doc is None or not doc.text.strip():
            return ""

        s = Summarizer(
            doc,
            keywords=self.keywords,
            max_chars=max_chars_override or self.max_chars_per_section
        )
        return s.summarize(n_sentences=n_sentences)

    def build_structured_summary(
        self,
        background_doc,
        hypothesis_doc,
        methodology_doc,
        outcomes_doc,
        impact_doc,
        n_sent_background=1,
        n_sent_hypothesis=1,
        n_sent_methodology=2,
        n_sent_outcomes=1,
        n_sent_impact=1,
        max_chars_background=None,
        max_chars_hypothesis=None,
        max_chars_methodology=800,
        max_chars_outcomes=None,
        max_chars_impact=None,
    ):
        lines = []

        # Background
        bkg = self._summarize_section(
            background_doc,
            n_sentences=n_sent_background,
            max_chars_override=max_chars_background
        )
        if bkg:
            lines.append("Background:")
            lines.append(bkg)
            lines.append("")

        # Hypothesis
        hyp = self._summarize_section(
            hypothesis_doc,
            n_sentences=n_sent_hypothesis,
            max_chars_override=max_chars_hypothesis
        )
        if hyp:
            lines.append("Hypothesis:")
            lines.append(hyp)
            lines.append("")

        # Methodology (con más espacio por defecto)
        meth = self._summarize_section(
            methodology_doc,
            n_sentences=n_sent_methodology,
            max_chars_override=max_chars_methodology
        )
        if meth:
            lines.append("Methodology:")
            lines.append(meth)
            lines.append("")

        # Expected Outcomes
        out = self._summarize_section(
            outcomes_doc,
            n_sentences=n_sent_outcomes,
            max_chars_override=max_chars_outcomes
        )
        if out:
            lines.append("Expected outcomes:")
            lines.append(out)
            lines.append("")

        # Impact
        imp = self._summarize_section(
            impact_doc,
            n_sentences=n_sent_impact,
            max_chars_override=max_chars_impact
        )
        if imp:
            lines.append("Impact:")
            lines.append(imp)
            lines.append("")

        return "\n".join(lines)
