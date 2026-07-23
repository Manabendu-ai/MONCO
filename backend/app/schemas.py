from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProbabilityBreakdown(BaseModel):
    glioma: float
    meningioma: float
    pituitary: float
    notumor: float


class PredictionResponse(BaseModel):
    id: Optional[int] = None
    prediction: str
    confidence: float
    probabilities: ProbabilityBreakdown
    explanation: Optional[str] = None
    image_path: Optional[str] = None
    created_at: Optional[datetime] = None


class HistoryItem(BaseModel):
    id: int
    user_id: Optional[int] = None
    image_path: str
    prediction: str
    confidence: float
    probabilities: ProbabilityBreakdown
    explanation: Optional[str] = None
    created_at: Optional[datetime] = None
