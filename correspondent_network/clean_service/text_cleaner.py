import logging
import re


class TextCleaner:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def clean(self, text: str) -> str:
        try:
            cleaned = re.sub(r"[^\w\s]", " ", text)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            self.logger.info(f"Text cleaned: {len(text)} -> {len(cleaned)} chars")
            return cleaned
        except Exception as e:
            self.logger.error(f"Text cleaning failed: {e}")
            raise
