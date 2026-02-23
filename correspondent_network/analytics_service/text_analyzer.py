import logging


class TextAnalyzer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def analyze(self, text: str) -> dict:
        try:
            words = text.split()
            word_count = len(words)
            char_count = len(text)
            avg_word_length = (
                sum(len(w) for w in words) / word_count if word_count > 0 else 0
            )
            unique_words = len(set(w.lower() for w in words))
            metrics = {
                "word_count": word_count,
                "char_count": char_count,
                "unique_words": unique_words,
                "avg_word_length": round(avg_word_length, 2),
            }
            self.logger.info(f"Analytics computed: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"TextAnalyzer failed: {e}")
            raise
