import os


class GridFSConfig:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        if not self.mongo_uri:
            raise ValueError("MONGO_URI is required")
