import hashlib
import logging
import os
from PIL import Image


class MetadataExtractor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extract_metadata(self, image_path: str) -> dict:
        try:
            file_size = os.path.getsize(image_path)
            with Image.open(image_path) as img:
                width, height = img.size
                fmt = img.format

            metadata = {
                "file_name": os.path.basename(image_path),
                "file_size": file_size,
                "width": width,
                "height": height,
                "format": fmt,
            }
            self.logger.info(f"Metadata extracted for {image_path}")
            return metadata
        except Exception as e:
            self.logger.error(f"Metadata extraction failed for {image_path}: {e}")
            raise

    def generate_image_id(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            content = f.read()
        image_id = hashlib.sha256(content).hexdigest()[:16]
        self.logger.info(f"Generated image_id={image_id} for {image_path}")
        return image_id
