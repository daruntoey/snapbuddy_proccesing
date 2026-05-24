"""Photographer schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class PhotographerResponse(BaseModel):
    id: int
    business_name: str
    bio: str | None
    location: str
    hourly_rate: int
    average_rating: float
    total_reviews: int
    primary_styles: List[str]
    profile_image: str | None

    class Config:
        from_attributes = True
