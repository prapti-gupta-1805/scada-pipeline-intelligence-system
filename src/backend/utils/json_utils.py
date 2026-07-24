from __future__ import annotations

from typing import Any

import numpy as np


def to_python_primitive(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): to_python_primitive(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_python_primitive(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return [to_python_primitive(item) for item in value.tolist()]
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    return value
