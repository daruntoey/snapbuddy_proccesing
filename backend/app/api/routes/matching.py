"""Photographer matching routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.matching import MatchRequest, MatchResponse
from app.services.matching_service import matching_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/match-photographers", response_model=MatchResponse)
async def match_photographers(
    request: MatchRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Find and rank matching photographers."""
    return await matching_service.find_matches(request, current_user.id, db)

@router.get("/recommendations/{mood_spec_id}")
async def get_recommendations(
    mood_spec_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get saved recommendations."""
    return await matching_service.get_saved_recommendations(mood_spec_id, current_user.id, db)
