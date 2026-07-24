from fastapi import APIRouter, HTTPException

from backend.schemas.fault import FaultFeatures
from backend.services import fault_service
from backend.utils.json_utils import to_python_primitive
from backend.utils.response import success_response

router = APIRouter()


@router.post("/predict-fault")
def predict_fault(payload: FaultFeatures):
    try:
        features = payload.model_dump()
        explain = features.pop("explain", True)
        result = fault_service.predict(features, explain=explain)
        return success_response({"prediction": to_python_primitive(result)}, message="Fault classification inference completed")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
