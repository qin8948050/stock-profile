from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from services.valuation.constants import ValuationMetricType

class ValuationRequest(BaseModel):
    metric_code: ValuationMetricType
    inputs: Dict[str, Any]  # 例如: {"growth_rate": 15.5, "pe_ratio": 20.0}

class ValuationResponse(BaseModel):
    id: int
    metric_code: str
    value: float
    input_params: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
