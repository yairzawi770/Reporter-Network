import logging
from storage import GridFSStorage


class MongoLoaderOrchestrator:
    def __init__(self, storage: GridFSStorage, logger: logging.Logger):
        self.storage = storage
        self.logger = logger

    def handle_upload(self, file_stream, image_id: str) -> str:
        self.logger.info(f"Handling upload for image_id={image_id}")
        return self.storage.save(file_stream, image_id)
