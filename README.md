# SCADA Pipeline Intelligence System

> Full-stack SCADA analytics for pipeline operations, fault classification, anomaly detection, and predictive maintenance.

---

## Overview

This project is a proof-of-concept SCADA analytics platform with a React dashboard frontend and a FastAPI backend. It demonstrates how telemetry inputs can be used to infer fault conditions, detect anomalous observations, and estimate maintenance risk using machine learning inference modules.

---

## Features

- Fault classification from SCADA measurements
- Anomaly detection using Isolation Forest scoring
- Predictive maintenance condition prediction with XGBoost
- React + Vite dashboard with model input forms and results panels
- FastAPI backend with health checks and metadata endpoints
- SHAP-based feature explainability in model inference modules

---

## Architecture

The repository is organized into separate layers:

- **Frontend:** `frontend/` contains a React application built with Vite and Tailwind CSS.
- **Backend:** `backend/` contains a FastAPI server exposing inference routes and metadata.
- **Models:** `models/` contains inference scripts and serialized model artifacts for each workflow.
- **Data:** `data/` contains sample CSV datasets used for model development.

Runtime flow:
1. The user interacts with the React dashboard.
2. The frontend sends JSON payloads to FastAPI endpoints under `/api/v1`.
3. The backend validates inputs using Pydantic schemas and loads the proper inference module.
4. The inference module returns prediction outputs and optional explainability information.

---

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- React Router DOM
- Axios
- Recharts
- Lucide React
- Framer Motion

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### Machine Learning

- scikit-learn
- XGBoost
- SHAP
- Isolation Forest
- Pandas
- NumPy
- Matplotlib

## Model Workflows

### Fault Classification

- Uses a serialized scikit-learn classifier and scaler.
- Inputs include pressure, flow rate, temperature, valve state, pump state, compressor state, energy consumption, and time metadata.
- Returns predicted fault category, class probabilities, confidence, and optional SHAP explanation.

### Anomaly Detection

- Uses a serialized Isolation Forest anomaly detector.
- Inputs are the same telemetry fields as the fault workflow.
- Returns anomaly status, anomaly score, normalized confidence, qualitative risk level, and top deviating features.

### Predictive Maintenance

- Uses a serialized XGBoost model with categorical encoders.
- Inputs include pipe size, thickness, material, grade, maximum pressure, temperature, corrosion impact, material loss, and operation years.
- Returns a condition prediction, confidence, risk level, class probabilities, and top contributing features.

---

## Project Structure

```bash
.
├── backend/
│   ├── api/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── app.py
│   └── config.py
├── data/
│   ├── market_pipe_thickness_loss_dataset.csv
│   └── scada_pipeline.csv
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── models/
│   ├── anomaly-detection/
│   ├── fault-classification/
│   └── predictive-maintenance/
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- pip

### Installation

```bash
git clone https://github.com/prapti-gupta-1805/scada-pipeline-intelligence-system.git
cd scada-pipeline-intelligence-system
```

### Running the Backend

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser, and verify the backend at `http://localhost:8000/api/v1`.

---

## API Documentation

### Base URL

`http://localhost:8000/api/v1`

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend and loaded model status |
| GET | `/metadata` | Feature metadata for UI forms |
| POST | `/predict-fault` | Fault classification inference |
| POST | `/predict-anomaly` | Anomaly detection inference |
| POST | `/predict-maintenance` | Predictive maintenance inference |

---

## API Payloads

### Fault / Anomaly Request Body

```json
{
  "pressure": 345.2,
  "flow_rate": 12.4,
  "temperature": 78.9,
  "valve_status": 1,
  "pump_state": 1,
  "pump_speed": 3200,
  "compressor_state": 1,
  "energy_consumption": 4.5,
  "hour": 14,
  "day_of_week": 3,
  "day_of_month": 18,
  "explain": true
}
```

### Predictive Maintenance Request Body

```json
{
  "Pipe_Size_mm": 800,
  "Thickness_mm": 25.78,
  "Material": "Stainless Steel",
  "Grade": "ASTM A333 Grade 6",
  "Max_Pressure_psi": 150,
  "Temperature_C": 11.6,
  "Corrosion_Impact_Percent": 18.68,
  "Thickness_Loss_mm": 0.53,
  "Material_Loss_Percent": 2.06,
  "Time_Years": 1,
  "explain": true
}
```

### Example Response Structure

The backend wraps responses with `success`, `message`, and `data` fields. Example `data` payload for fault classification:

```json
{
  "prediction": {
    "predicted_class": "Leak",
    "predicted_class_id": 1,
    "confidence": 0.88,
    "class_probabilities": {
      "Normal": 0.05,
      "Leak": 0.88,
      "Blockage": 0.03,
      "Surge": 0.02,
      "Degradation": 0.02
    },
    "raw_sample": { ... },
    "shap_explanation": {
      "plot_path": "...",
      "top_features": [ ... ]
    }
  }
}
```

---

## Notes

- The backend loads model inference modules at startup from `backend/utils/model_loader.py`.
- Inference requires serialized model artifacts to be present under `models/<workflow>/`.
- The frontend uses Axios with a base URL of `http://localhost:8000/api/v1`.

---

## Future Improvements

- Add Docker and CI/CD configuration
- Add authentication and user roles
- Add historical telemetry charts and alerting workflows
- Improve model retraining pipelines with production data
- Add automated tests for backend endpoints and frontend flows

---

## Contributing

Contributions are welcome. Please open issues or pull requests for bug fixes, feature enhancements, and documentation improvements.

---

## License

This repository does not include a license file. Please add one if you plan to publish or share the project publicly.

---

## Author

Prapti Gupta

GitHub: https://github.com/prapti-gupta-1805

LinkedIn: https://www.linkedin.com/in/prapti-gupta/
