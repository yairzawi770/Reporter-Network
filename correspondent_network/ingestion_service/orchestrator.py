import logging
import os
from config import IngestionConfig
from ocr_engine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_loader_client import MongoLoaderClient
from kafka_publisher import KafkaPublisher

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


class IngestionOrchestrator:
    def __init__(
        self,
        config: IngestionConfig,
        ocr_engine: OCREngine,
        metadata_extractor: MetadataExtractor,
        mongo_client: MongoLoaderClient,
        publisher: KafkaPublisher,
        logger: logging.Logger,
    ):
        self.config = config
        self.ocr_engine = ocr_engine
        self.metadata_extractor = metadata_extractor
        self.mongo_client = mongo_client
        self.publisher = publisher
        self.logger = logger

    def process_image(self, image_path: str):
        self.logger.info(f"Processing image: {image_path}")
        image_id = self.metadata_extractor.generate_image_id(image_path)
        metadata = self.metadata_extractor.extract_metadata(image_path)
        raw_text = self.ocr_engine.extract_text(image_path)
        self.mongo_client.send(image_path, image_id)
        event = {
            "image_id": image_id,
            "raw_text": raw_text,
            "metadata": metadata,
        }
        self.publisher.publish(event)
        self.logger.info(f"Finished processing image_id={image_id}")

    def run(self):
        self.logger.info(f"Scanning directory: {self.config.image_directory}")
        files = [
            f for f in os.listdir(self.config.image_directory)
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        ]
        self.logger.info(f"Found {len(files)} image(s)")
        for filename in files:
            full_path = os.path.join(self.config.image_directory, filename)
            try:
                self.process_image(full_path)
            except Exception as e:
                self.logger.error(f"Failed to process {full_path}: {e}")
        self.logger.info("Ingestion run complete")
