import logging
import requests


class MongoLoaderClient:
    def __init__(self, mongo_loader_url: str, logger: logging.Logger):
        self.mongo_loader_url = mongo_loader_url
        self.logger = logger

    def send(self, file_path: str, image_id: str) -> bool:
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = {"image_id": image_id}
                response = requests.post(
                    f"{self.mongo_loader_url}/upload", files=files, data=data, timeout=30
                )
            response.raise_for_status()
            self.logger.info(f"Uploaded {file_path} with image_id={image_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload {file_path}: {e}")
            raise
