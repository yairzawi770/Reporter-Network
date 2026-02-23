import logging
import os
from config import IngestionConfig
from ocr_engine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_loader_client import MongoLoaderClient
from kafka_publisher import KafkaPublisher
from orchestrator import IngestionOrchestrator


def main():
    config = IngestionConfig()
    config.validate()

    logger = logging.getLogger("ingestion-service")
    logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

    ocr_engine = OCREngine(logger)
    metadata_extractor = MetadataExtractor(logger)
    mongo_client = MongoLoaderClient(config.mongo_loader_url, logger)
    publisher = KafkaPublisher(config.bootstrap_servers, config.raw_topic, logger)

    orchestrator = IngestionOrchestrator(
        config, ocr_engine, metadata_extractor, mongo_client, publisher, logger
    )
    orchestrator.run()


if __name__ == "__main__":
    main()
