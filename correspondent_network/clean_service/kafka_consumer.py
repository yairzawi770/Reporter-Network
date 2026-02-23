import json
import logging
from kafka import KafkaConsumer as _KafkaConsumer


class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic_name: str,
        group_id: str,
        logger: logging.Logger,
    ):
        self.topic_name = topic_name
        self.logger = logger
        self.consumer = _KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def start(self, callback):
        self.logger.info(f"Listening on topic: {self.topic_name}")
        for message in self.consumer:
            self.logger.info(f"Received event: image_id={message.value.get('image_id')}")
            try:
                callback(message.value)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
