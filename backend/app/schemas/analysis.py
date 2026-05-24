"""Analysis schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class MoodAnalysisRequest(BaseModel):
    text_description: str | None = None
    image_urls: List[str] = []
    budget_min: int | None = None
    budget_max: int | None = None
    location: str | None = None

class MoodAnalysisResponse(BaseModel):
    mood_spec_id: int
    mood_tags: List[str]
    style_tags: List[str]
    detected_intent: str
    aesthetic_summary: str
