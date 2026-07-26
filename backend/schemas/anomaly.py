from pydantic import BaseModel, Field
from typing import Optional


class AnomalyFeatures(BaseModel):
    pressure: float
    flow_rate: float
    temperature: float
    valve_status: int
    pump_state: int
    pump_speed: float
    compressor_state: int
    energy_consumption: float
    hour: int
    day_of_week: int
    day_of_month: int
    explain: Optional[bool] = Field(True, description="Return explanation of top deviating features")
