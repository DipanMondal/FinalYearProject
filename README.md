# Final Year Project

## Project Structure:
```
climate-intelligence-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── pipelines/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── artifacts/
│   ├── logs/
│   ├── models_store/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── utils/
│   └── Home.py
│
├── notebooks/
├── tests/
├── docs/
└── README.md
```
---
## Sample .env
```
APP_NAME=Climate Intelligence Platform

DB_PATH=backend/data/climate.db

ARTIFACTS_DIR=backend/artifacts
MODELS_DIR=backend/models_store
LOGS_DIR=backend/logs

API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True
```
---
## DATA INGESTION PIPELINE
```
State Name
    ↓
Coordinate Resolver
    ↓
NASA POWER API Client
    ↓
Response Validation
    ↓
Transformation Layer
    ↓
Database Storage
    ↓
Metadata Generation
    ↓
State Lifecycle Update
    ↓
Pipeline Logging
```
---
## TRAINING PIPELINE
```
State
   ↓
Load Engineered Features
   ↓
Train/Test Split
   ↓
SARIMAX Grid Search
   ↓
Evaluate Metrics
   ↓
Save Model
   ↓
Update Model Registry
   ↓
Update State Status
   ↓
Pipeline Logging
```