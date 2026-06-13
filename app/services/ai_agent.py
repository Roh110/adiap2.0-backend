from pydantic import BaseModel
from typing import Optional


class AIDecision(BaseModel):
    status: str
    risk_level: str
    confidence: int
    downtime_estimation_hours: int
    recommendation: str
    root_cause: str
    action_priority: str