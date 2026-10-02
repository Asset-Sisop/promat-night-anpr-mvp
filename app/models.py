from pydantic import BaseModel, Field
from typing import Optional

class BBox(BaseModel):
    x: int
    y: int
    width: int
    height: int

class RecognitionResponse(BaseModel):
    plate: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: Optional[BBox] = None
    frame: Optional[str] = None
    timestamp: str
    processing_ms: float
    candidates: list[str] = []
    status: str = "ok"
    message: Optional[str] = None
