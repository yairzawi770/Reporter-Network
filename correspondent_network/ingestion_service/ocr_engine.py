import logging
import pytesseract
from PIL import Image


class OCREngine:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extract_text(self, image_path: str) -> str:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            self.logger.info(f"OCR extracted {len(text)} chars from {image_path}")
            return text.strip()
        except Exception as e:
            self.logger.error(f"OCR failed for {image_path}: {e}")
            raise
