import logging
from config import CleanConfig
from kafka_consumer import KafkaConsumer
from text_cleaner import TextCleaner
from kafka_publisher import KafkaPublisher
from orchestrator import CleanOrchestrator


def main():
    config = CleanConfig()
    config.validate()

    logger = logging.getLogger("clean-service")
    logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

    consumer = KafkaConsumer(config.bootstrap_servers, config.raw_topic, config.group_id, logger)
    cleaner = TextCleaner(logger)
    publisher = KafkaPublisher(config.bootstrap_servers, config.clean_topic, logger)

    orchestrator = CleanOrchestrator(consumer, cleaner, publisher, logger)
    orchestrator.run()


if __name__ == "__main__":
    main()
