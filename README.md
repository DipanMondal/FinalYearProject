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

## Sample backend\.env
```
APP_NAME=Climate Intelligence Platform

DB_PATH=backend/data/climate.db

ARTIFACTS_DIR=backend/artifacts
MODELS_DIR=backend/models_store
LOGS_DIR=backend/logs

API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True

GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.2
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

---

## FORECASTING PIPELINE
```
Load historical features
       ↓
Predict next month
       ↓
Append prediction to dataframe
       ↓
Recompute rolling features
       ↓
Recompute lag features
       ↓
Generate next seasonal encoding
       ↓
Predict next month
       ↓
Repeat recursively
```
---

## FRONTEND & DASHBOARD
```
Dashboard/
│
├── Home Page
│
├── State Overview
│
├── Seasonal Climate Explorer
│
├── Climate Change Trends
│
├── Extreme Events & Risk
│
├── Forecasting Center
│
└── Data & Model Management
```
---

```
frontend/

├── app.py

├── pages/

│   ├── 1_Home.py
│   ├── 2_State_Overview.py
│   ├── 3_Seasonal_Explorer.py
│   ├── 4_Climate_Trends.py
│   ├── 5_Extreme_Events.py
│   ├── 6_Forecasting.py
│   └── 7_Data_Management.py

├── services/
│   └── api_client.py

├── components/
│   ├── sidebar.py
│   ├── kpi_cards.py
│   └── charts.py

├── utils/
│   ├── constants.py
│   └── helpers.py

├── assets/
│
└── .streamlit/
    └── config.toml
```