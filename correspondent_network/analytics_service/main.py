import logging
from config import AnalyticsConfig
from kafka_consumer import KafkaConsumer
from text_analyzer import TextAnalyzer
from kafka_publisher import KafkaPublisher
from orchestrator import AnalyticsOrchestrator


def main():
    config = AnalyticsConfig()
    config.validate()

    logger = logging.getLogger("analytics-service")
    logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

    consumer = KafkaConsumer(config.bootstrap_servers, config.clean_topic, config.group_id, logger)
    analyzer = TextAnalyzer(logger)
    publisher = KafkaPublisher(config.bootstrap_servers, config.analytics_topic, logger)

    orchestrator = AnalyticsOrchestrator(consumer, analyzer, publisher, logger)
    orchestrator.run()


if __name__ == "__main__":
    main()
