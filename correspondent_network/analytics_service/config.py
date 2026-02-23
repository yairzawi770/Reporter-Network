import os


class AnalyticsConfig:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.clean_topic = os.getenv("CLEAN_TOPIC", "clean")
        self.analytics_topic = os.getenv("ANALYTICS_TOPIC", "analytics")
        self.group_id = os.getenv("GROUP_ID", "analytics-service-group")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        if not self.bootstrap_servers:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS is required")
