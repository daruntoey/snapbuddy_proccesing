"""Matching routes — powered by real buddyProfile + buddyPortfolio data."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger

from app.services.ai_matching_service import ai_matching_service

router = APIRouter()


class MatchRequest(BaseModel):
    text_description: str
    budget_max: Optional[int] = None
    city: Optional[str] = None
    min_rating: Optional[float] = None
    top_k: int = 10


@router.post("/match")
async def match_buddies(request: MatchRequest):
    """
    AI-powered buddy matching.
    - Reads buddyProfile + buddyPortfolio from Google Sheets
    - Ranks by NLP cosine similarity + rating + experience
    - Adds Gemini explanations for top 5
    """
    if not request.text_description or not request.text_description.strip():
        raise HTTPException(status_code=400, detail="text_description is required")

    logger.info(f"🔍 Match request: '{request.text_description[:80]}'")
    try:
        matches = await ai_matching_service.match_buddies(
            user_description=request.text_description,
            budget_max=request.budget_max,
            city=request.city,
            min_rating=request.min_rating,
            top_k=request.top_k,
        )
        return {
            "matches": matches,
            "total": len(matches),
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Matching error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
