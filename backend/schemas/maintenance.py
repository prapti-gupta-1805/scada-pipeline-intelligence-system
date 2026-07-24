from pydantic import BaseModel, Field
from typing import Optional


class MaintenanceFeatures(BaseModel):
    Pipe_Size_mm: float
    Thickness_mm: float
    Material: str
    Grade: str
    Max_Pressure_psi: float
    Temperature_C: float
    Corrosion_Impact_Percent: float
    Thickness_Loss_mm: float
    Material_Loss_Percent: float
    Time_Years: float
    explain: Optional[bool] = Field(True, description="Return SHAP explanations")
