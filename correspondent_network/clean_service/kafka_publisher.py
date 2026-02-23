import json
import logging
from kafka import KafkaProducer


class KafkaPublisher:
    def __init__(self, bootstrap_servers: str, topic_name: str, logger: logging.Logger):
        self.topic_name = topic_name
        self.logger = logger
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish(self, event: dict):
        try:
            self.producer.send(self.topic_name, value=event)
            self.producer.flush()
            self.logger.info(f"Published CLEAN event: image_id={event.get('image_id')}")
        except Exception as e:
            self.logger.error(f"Failed to publish event: {e}")
            raise
