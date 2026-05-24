"""Matching schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class MatchRequest(BaseModel):
    mood_spec_id: int
    limit: int = 10

class PhotographerMatch(BaseModel):
    photographer_id: int
    business_name: str
    match_score: float
    style_similarity_score: float
    explanation: str
    profile_image: str | None
    hourly_rate: int
    average_rating: float
    location: str

class MatchResponse(BaseModel):
    matches: List[PhotographerMatch]
    total: int
