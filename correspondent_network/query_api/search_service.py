import logging
from elasticsearch import Elasticsearch


class SearchService:
    def __init__(self, es_client: Elasticsearch, index_name: str, logger: logging.Logger):
        self.es = es_client
        self.index_name = index_name
        self.logger = logger

    def search(self, filters: dict) -> list:
        query_text = filters.get("q", "")
        size = filters.get("size", 10)

        if query_text:
            query = {
                "query": {
                    "multi_match": {
                        "query": query_text,
                        "fields": ["raw_text", "clean_text"],
                    }
                },
                "size": size,
            }
        else:
            query = {"query": {"match_all": {}}, "size": size}

        try:
            response = self.es.search(index=self.index_name, body=query)
            hits = response["hits"]["hits"]
            self.logger.info(f"Search for '{query_text}' returned {len(hits)} results")
            return [hit["_source"] for hit in hits]
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            raise
