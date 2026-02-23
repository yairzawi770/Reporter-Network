import logging
from fastapi import FastAPI, Query as QParam
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch
from config import APIConfig
from search_service import SearchService

config = APIConfig()
config.validate()

logger = logging.getLogger("query-api")
logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

es_client = Elasticsearch(config.es_uri)
search_service = SearchService(es_client, config.es_index, logger)

app = FastAPI(title="Query API")


@app.get("/search")
def search_endpoint(q: str = QParam(default="", description="Search query"), size: int = 10):
    try:
        results = search_service.search({"q": q, "size": size})
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Search endpoint error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
