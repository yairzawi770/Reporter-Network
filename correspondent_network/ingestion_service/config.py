import os


class IngestionConfig:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.raw_topic = os.getenv("RAW_TOPIC", "raw")
        self.image_directory = os.getenv("IMAGE_DIRECTORY", "./images")
        self.mongo_loader_url = os.getenv("MONGO_LOADER_URL", "http://localhost:8001")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        if not self.image_directory:
            raise ValueError("IMAGE_DIRECTORY is required")
        if not self.mongo_loader_url:
            raise ValueError("MONGO_LOADER_URL is required")
