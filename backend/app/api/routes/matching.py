"""AI Matching routes."""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_matching_service import ai_matching_service

router = APIRouter()


class MatchRequest(BaseModel):
    description: str
    budget_max: int = 10000
    location: str = "Bangkok"


@router.post("/match")
async def match_photographers(request: MatchRequest):
    # ✅ ไม่มี current_user parameter
    """Match photographers using AI + Google Sheets data."""
    matches = await ai_matching_service.match_photographers(
        user_description=request.description,
        budget_max=request.budget_max,
        location=request.location
    )
    
    return {
        "matches": matches,
        "total": len(matches),
        "query": request.description
    }
