import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    ocr_min_confidence: float = float(os.getenv("OCR_MIN_CONFIDENCE", "0.35"))
    plate_min_area: int = int(os.getenv("PLATE_MIN_AREA", "800"))
    plate_max_area: int = int(os.getenv("PLATE_MAX_AREA", "120000"))
    plate_min_ratio: float = float(os.getenv("PLATE_MIN_RATIO", "2.0"))
    plate_max_ratio: float = float(os.getenv("PLATE_MAX_RATIO", "7.0"))
    max_processing_ms: int = int(os.getenv("MAX_PROCESSING_MS", "500"))
    jpeg_quality: int = int(os.getenv("JPEG_QUALITY", "90"))
    tesseract_cmd: str = os.getenv("TESSERACT_CMD", "")
    max_candidates: int = int(os.getenv("MAX_CANDIDATES", "12"))

settings = Settings()
