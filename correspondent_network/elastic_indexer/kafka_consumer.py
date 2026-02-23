import json
import logging
from kafka import KafkaConsumer as _KafkaConsumer


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, topics_list: list, group_id: str, logger: logging.Logger):
        self.topics_list = topics_list
        self.logger = logger
        self.consumer = _KafkaConsumer(
            *topics_list,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def start(self, callback):
        self.logger.info(f"Listening on topics: {self.topics_list}")
        for message in self.consumer:
            self.logger.info(f"Received event from {message.topic}: image_id={message.value.get('image_id')}")
            try:
                callback(message.topic, message.value)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
