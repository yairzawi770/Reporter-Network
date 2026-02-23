import logging
from kafka_consumer import KafkaConsumer
from es_client import ElasticsearchClient


class IndexOrchestrator:
    def __init__(self, consumer: KafkaConsumer, es_client: ElasticsearchClient, logger: logging.Logger):
        self.consumer = consumer
        self.es_client = es_client
        self.logger = logger

    def handle_event(self, topic: str, event: dict):
        image_id = event.get("image_id")
        self.logger.info(f"Indexing event from topic={topic} for image_id={image_id}")

        if topic == "raw":
            document = {
                "image_id": image_id,
                "raw_text": event.get("raw_text"),
                "metadata": event.get("metadata", {}),
            }
        elif topic == "clean":
            document = {"clean_text": event.get("clean_text")}
        elif topic == "analytics":
            document = {"analytics": event.get("analytics", {})}
        else:
            self.logger.error(f"Unknown topic: {topic}")
            return

        self.es_client.upsert(document, image_id)

    def run(self):
        self.logger.info("IndexOrchestrator starting")
        self.consumer.start(self.handle_event)
