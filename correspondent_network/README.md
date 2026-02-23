# מבצע "רשת הכתבים" – Correspondent Network

An event-driven pipeline for processing tweet images via OCR, text cleaning, analytics, and full-text search.

## Architecture

```
Images → Ingestion Service → [Kafka: raw] → Clean Service → [Kafka: clean] → Analytics Service → [Kafka: analytics]
                ↓                                                                                         ↓
         GridFS (MongoDB)                                                               Elastic Indexer → Elasticsearch
                                                                                                              ↓
                                                                                              Query API → Dashboard
```

## Services

| Service | Port | Role |
|---|---|---|
| `gridfs_service` | 8001 | Stores binary images in MongoDB via GridFS |
| `ingestion_service` | — | Scans image folder, runs OCR, publishes RAW event |
| `clean_service` | — | Consumes RAW, cleans text, publishes CLEAN |
| `analytics_service` | — | Consumes CLEAN, computes metrics, publishes ANALYTICS |
| `elastic_indexer` | — | Consumes all topics, upserts to Elasticsearch |
| `query_api` | 8002 | REST search over Elasticsearch |
| `dashboard` | 8501 | Streamlit UI |

## Quick Start

### 1. Set your images directory

```powershell
Copy-Item .env.example .env
# Open .env and set IMAGE_DIRECTORY to your images folder
# e.g. IMAGE_DIRECTORY=C:\Users\YourName\Downloads
notepad .env
```

### 2. Start the full stack

```powershell
$env:IMAGE_DIRECTORY = "$env:USERPROFILE\Downloads"
docker-compose up --build
```

### 3. Run ingestion

The ingestion service runs once and processes all images in `IMAGE_DIRECTORY`. To re-run:

```powershell
docker-compose run --rm ingestion_service
```

### 4. Open the dashboard

Visit [http://localhost:8501](http://localhost:8501)

## Local Development (without Docker)

```powershell
# Start infrastructure only
docker-compose up zookeeper kafka mongodb elasticsearch

# In each service directory:
pip install -r requirements.txt
python main.py
```

## Useful PowerShell Commands

```powershell
# View logs for a specific service
docker-compose logs -f ingestion_service

# Stop everything
docker-compose down

# Stop and remove all volumes (clean slate)
docker-compose down -v

# Rebuild a single service
docker-compose up --build clean_service

# Check running containers
docker-compose ps
```

## Folder Structure

```
correspondent_network/
├── docker-compose.yml
├── .env.example
├── ingestion_service/     # OCR + metadata + Kafka RAW publisher
├── gridfs_service/        # FastAPI + MongoDB GridFS storage
├── clean_service/         # Text cleaning consumer/publisher
├── analytics_service/     # Text analytics consumer/publisher
├── elastic_indexer/       # Elasticsearch upsert consumer
├── query_api/             # FastAPI search API
└── dashboard/             # Streamlit UI
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `IMAGE_DIRECTORY` | `./images` | Path to folder containing tweet images |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker |
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection |
| `MONGO_LOADER_URL` | `http://localhost:8001` | GridFS service URL |
| `ES_URI` | `http://localhost:9200` | Elasticsearch URL |
| `ES_INDEX` | `tweets` | Elasticsearch index name |
| `LOG_LEVEL` | `INFO` | Logging level |
