import logging
from pymongo import MongoClient
import gridfs


class GridFSStorage:
    def __init__(self, mongo_uri: str, logger: logging.Logger):
        self.logger = logger
        self.client = MongoClient(mongo_uri)
        self.db = self.client["correspondent_network"]
        self.fs = gridfs.GridFS(self.db)

    def save(self, file_stream, image_id: str) -> str:
        try:
            existing = self.db.fs.files.find_one({"filename": image_id})
            if existing:
                self.logger.info(f"File already exists for image_id={image_id}, skipping")
                return image_id

            self.fs.put(file_stream, filename=image_id)
            self.logger.info(f"Saved file to GridFS with image_id={image_id}")
            return image_id
        except Exception as e:
            self.logger.error(f"GridFS save failed for image_id={image_id}: {e}")
            raise
