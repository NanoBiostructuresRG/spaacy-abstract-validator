# summarizer.py 

class Summarizer:
    def __init__(self, doc, keywords=None, max_chars=1200):
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
        self.calculate_frequencies()
        self.score_sentences()
        summarized = sorted(self.sentence_scores, key=self.sentence_scores.get, reverse=True)
        summarized = summarized[:n_sentences]
        summarized = sorted(summarized, key=lambda s: s.start)  # keep orden original
        summary_text = " ".join([sent.text for sent in summarized])

        # Restricted up to 1200 characters (with spaces)
        if len(summary_text) > self.max_chars:
            cutoff_point = summary_text.rfind(" ", 0, self.max_chars)
            if cutoff_point == -1:
                cutoff_point = self.max_chars
            summary_text = summary_text[:cutoff_point].rstrip() + "..."

        return summary_text
