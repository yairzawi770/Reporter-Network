import logging
from kafka_consumer import KafkaConsumer
from text_cleaner import TextCleaner
from kafka_publisher import KafkaPublisher


class CleanOrchestrator:
    def __init__(
        self,
        consumer: KafkaConsumer,
        cleaner: TextCleaner,
        publisher: KafkaPublisher,
        logger: logging.Logger,
    ):
        self.consumer = consumer
        self.cleaner = cleaner
        self.publisher = publisher
        self.logger = logger

    def handle_event(self, event: dict):
        image_id = event.get("image_id")
        raw_text = event.get("raw_text", "")
        self.logger.info(f"Cleaning text for image_id={image_id}")
        clean_text = self.cleaner.clean(raw_text)
        clean_event = {
            "image_id": image_id,
            "raw_text": raw_text,
            "clean_text": clean_text,
            "metadata": event.get("metadata", {}),
        }
        self.publisher.publish(clean_event)

    def run(self):
        self.logger.info("CleanOrchestrator starting")
        self.consumer.start(self.handle_event)
