import os


class APIConfig:
    def __init__(self):
        self.es_uri = os.getenv("ES_URI", "http://localhost:9200")
        self.es_index = os.getenv("ES_INDEX", "tweets")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        if not self.es_uri:
            raise ValueError("ES_URI is required")
