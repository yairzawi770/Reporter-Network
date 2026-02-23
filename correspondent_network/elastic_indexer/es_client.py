import logging
from elasticsearch import Elasticsearch


class ElasticsearchClient:
    def __init__(self, es_uri: str, index_name: str, logger: logging.Logger):
        self.index_name = index_name
        self.logger = logger
        self.es = Elasticsearch(es_uri)

    def upsert(self, document: dict, image_id: str):
        try:
            self.es.update(
                index=self.index_name,
                id=image_id,
                body={"doc": document, "doc_as_upsert": True},
            )
            self.logger.info(f"Upserted document for image_id={image_id}")
        except Exception as e:
            self.logger.error(f"Elasticsearch upsert failed for image_id={image_id}: {e}")
            raise

    def search(self, query: dict) -> list:
        try:
            response = self.es.search(index=self.index_name, body=query)
            return response["hits"]["hits"]
        except Exception as e:
            self.logger.error(f"Elasticsearch search failed: {e}")
            raise
