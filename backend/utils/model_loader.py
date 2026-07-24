"""Cached loader for existing inference modules.

This module loads model modules exactly once and exposes a simple API for the
backend services. It never reimplements inference logic.
"""
from pathlib import Path
import importlib.util
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]

_cache: dict[str, ModuleType] = {}


def _load_module_from_path(module_name: str, file_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def initialize_models() -> dict[str, str | None]:
    """Load each inference module exactly once and return their availability."""
    modules = {
        "predictive_maintenance": ("maintenance", ROOT / "models" / "predictive-maintenance" / "pm-inference.py"),
        "anomaly_detection": ("anomaly", ROOT / "models" / "anomaly-detection" / "ad-inference.py"),
        "fault_classification": ("fault", ROOT / "models" / "fault-classification" / "fc-inference.py"),
    }

    availability = {}
    for name, (cache_key, file_path) in modules.items():
        try:
            if cache_key not in _cache:
                _cache[cache_key] = _load_module_from_path(cache_key, file_path)
            availability[name] = str(file_path)
        except Exception as exc:
            availability[name] = None
            if cache_key in _cache:
                del _cache[cache_key]
            setattr(sys.modules[__name__], "last_error", str(exc))
    return availability


def get_maintenance_module() -> ModuleType:
    if "maintenance" not in _cache:
        initialize_models()
    return _cache["maintenance"]


def get_anomaly_module() -> ModuleType:
    if "anomaly" not in _cache:
        initialize_models()
    return _cache["anomaly"]


def get_fault_module() -> ModuleType:
    if "fault" not in _cache:
        initialize_models()
    return _cache["fault"]


def get_model_status() -> dict[str, object]:
    availability = initialize_models()
    return {
        "loaded": {name: value is not None for name, value in availability.items()},
        "artifacts": availability,
        "error": getattr(sys.modules[__name__], "last_error", None),
    }
