import logging
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from config import GridFSConfig
from storage import GridFSStorage
from orchestrator import MongoLoaderOrchestrator

config = GridFSConfig()
config.validate()

logger = logging.getLogger("gridfs-service")
logging.basicConfig(level=getattr(logging, config.log_level, logging.INFO))

storage = GridFSStorage(config.mongo_uri, logger)
orchestrator = MongoLoaderOrchestrator(storage, logger)

app = FastAPI(title="GridFS Service")


@app.post("/upload")
async def upload(file: UploadFile = File(...), image_id: str = Form(...)):
    try:
        content = await file.read()
        import io
        orchestrator.handle_upload(io.BytesIO(content), image_id)
        return JSONResponse({"status": "ok", "image_id": image_id})
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
