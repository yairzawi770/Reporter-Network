import logging
from config import IndexerConfig
from kafka_consumer import KafkaConsumer
from es_client import ElasticsearchClient
from orchestrator import IndexOrchestrator


def main():
    config = IndexerConfig()
    config.validate()

    logger = logging.getLogger("elastic-indexer")
    logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

    topics = [config.raw_topic, config.clean_topic, config.analytics_topic]
    consumer = KafkaConsumer(config.bootstrap_servers, topics, config.group_id, logger)
    es_client = ElasticsearchClient(config.es_uri, config.es_index, logger)

    orchestrator = IndexOrchestrator(consumer, es_client, logger)
    orchestrator.run()


if __name__ == "__main__":
    main()
