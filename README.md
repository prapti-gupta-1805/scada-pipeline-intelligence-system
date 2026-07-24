# SCADA Pipeline Intelligence System

An end-to-end SCADA analytics app for pipeline operations.

The project combines:
- A FastAPI backend that serves ML predictions
- A React/Vite frontend for dashboarding and inference
- Three model workflows for fault classification, anomaly detection, and predictive maintenance

## Features

- Predict pipeline faults from live feature input
- Detect anomalies in SCADA telemetry
- Estimate maintenance risk and remaining asset health
- View model summaries and feature visualizations in the frontend
- Check backend health and model availability through API endpoints

## Project Layout

- `backend/` FastAPI app, API routes, schemas, services, and utilities
- `frontend/` React app built with Vite and Tailwind CSS
- `models/` training and inference scripts for each ML task
- `data/` sample datasets used by the model pipelines

## Requirements

- Python 3.10+ recommended
- Node.js 18+ recommended
- `pip` and `npm`

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd scada-pipeline-intelligence-system
```

### 2. Set up the backend

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r backend/requirements.txt
pip install -r requirements.txt
```

Run the API server:

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Set up the frontend

Install dependencies and start the Vite dev server:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000/api/v1`.

## API Endpoints

Base path: `/api/v1`

- `GET /health` or `GET /api/v1/health` - backend and model status
- `GET /metadata` - feature metadata for the UI
- `POST /predict-fault` - fault classification inference
- `POST /predict-anomaly` - anomaly detection inference
- `POST /predict-maintenance` - predictive maintenance inference

## Input Notes

The API uses Pydantic schemas to validate payloads.

- Fault and anomaly predictions share the same telemetry-style fields
- Maintenance prediction uses asset and corrosion-related fields
- Each request supports an optional `explain` flag, which defaults to `true`

## Model Artifacts

The backend loads inference modules directly from the `models/` directory at startup. If a module fails to load, the `/health` response will report degraded status and include the load error.

## Frontend Pages

- `/` dashboard overview
- `/fault` fault classification
- `/anomaly` anomaly detection
- `/maintenance` predictive maintenance
- `/analytics` model and data analytics

## Development Tips

- If you move the backend off `localhost:8000`, update `frontend/src/lib/api.js`
- Visual assets for the model pages live in `frontend/public/models/`
- Sample datasets are available in `data/` for local experimentation

## License

No license file is currently included. Add one if you plan to publish or share the project publicly.
