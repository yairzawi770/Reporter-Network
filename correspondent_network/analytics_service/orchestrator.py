import logging
from kafka_consumer import KafkaConsumer
from text_analyzer import TextAnalyzer
from kafka_publisher import KafkaPublisher


class AnalyticsOrchestrator:
    def __init__(self, consumer: KafkaConsumer, analyzer: TextAnalyzer, publisher: KafkaPublisher, logger: logging.Logger):
        self.consumer = consumer
        self.analyzer = analyzer
        self.publisher = publisher
        self.logger = logger

    def handle_event(self, event: dict):
        image_id = event.get("image_id")
        clean_text = event.get("clean_text", "")
        self.logger.info(f"Analyzing text for image_id={image_id}")
        metrics = self.analyzer.analyze(clean_text)
        analytics_event = {
            "image_id": image_id,
            "raw_text": event.get("raw_text", ""),
            "clean_text": clean_text,
            "metadata": event.get("metadata", {}),
            "analytics": metrics,
        }
        self.publisher.publish(analytics_event)

    def run(self):
        self.logger.info("AnalyticsOrchestrator starting")
        self.consumer.start(self.handle_event)
