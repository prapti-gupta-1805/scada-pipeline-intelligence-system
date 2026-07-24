from typing import Dict, Any
from backend.utils import model_loader


def predict(features: Dict[str, Any], explain: bool = True) -> Dict[str, Any]:
    mod = model_loader.get_maintenance_module()
    try:
        return mod.predict(features, explain=explain)
    except ValueError as e:
        raise
    except Exception as e:
        raise
