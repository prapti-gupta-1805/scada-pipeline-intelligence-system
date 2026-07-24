import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure 'src' is on sys.path so 'backend' package imports resolve when running from repository root
HERE = Path(__file__).resolve()
SRC_DIR = str(HERE.parents[1])
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from backend.api import anomaly, fault, maintenance
from backend.utils import model_loader
from backend.utils.response import success_response

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="SCADA ML Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_models():
    try:
        model_loader.initialize_models()
        logger.info("All ML modules loaded successfully")
    except Exception as exc:
        logger.error("Error loading ML modules: %s", exc)


@app.get("/health")
def health():
    status = model_loader.get_model_status()
    return success_response(
        {
            "status": "ok" if any(status["loaded"].values()) else "degraded",
            "models": status["loaded"],
            "artifacts": status["artifacts"],
            "error": status["error"],
        },
        message="Backend health status",
    )


@app.get("/api/v1/metadata")
def metadata():
    return success_response(
        {
            "maintenance": {
                "features": [
                    "Pipe_Size_mm",
                    "Thickness_mm",
                    "Material",
                    "Grade",
                    "Max_Pressure_psi",
                    "Temperature_C",
                    "Corrosion_Impact_Percent",
                    "Thickness_Loss_mm",
                    "Material_Loss_Percent",
                    "Time_Years",
                ]
            },
            "anomaly": {
                "features": [
                    "segment_id",
                    "pressure",
                    "flow_rate",
                    "temperature",
                    "valve_status",
                    "pump_state",
                    "pump_speed",
                    "compressor_state",
                    "energy_consumption",
                    "alarm_triggered",
                    "hour",
                    "day_of_week",
                    "day_of_month",
                ]
            },
            "fault": {
                "features": [
                    "segment_id",
                    "pressure",
                    "flow_rate",
                    "temperature",
                    "valve_status",
                    "pump_state",
                    "pump_speed",
                    "compressor_state",
                    "energy_consumption",
                    "alarm_triggered",
                    "hour",
                    "day_of_week",
                    "day_of_month",
                ]
            },
        },
        message="Frontend metadata",
    )


app.include_router(maintenance.router, prefix="/api/v1")
app.include_router(anomaly.router, prefix="/api/v1")
app.include_router(fault.router, prefix="/api/v1")
