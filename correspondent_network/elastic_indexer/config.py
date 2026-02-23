import os

class IndexerConfig:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.raw_topic = os.getenv("RAW_TOPIC", "raw")
        self.clean_topic = os.getenv("CLEAN_TOPIC", "clean")
        self.analytics_topic = os.getenv("ANALYTICS_TOPIC", "analytics")
        self.group_id = os.getenv("GROUP_ID", "elastic-indexer-group")
        self.es_uri = os.getenv("ES_URI", "http://localhost:9200")
        self.es_index = os.getenv("ES_INDEX", "tweets")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        if not self.es_uri:
            raise ValueError("ES_URI is required")
