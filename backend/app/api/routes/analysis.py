"""AI analysis routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.analysis import MoodAnalysisRequest, MoodAnalysisResponse
from app.services.analysis_service import analysis_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/mood", response_model=MoodAnalysisResponse)
async def analyze_mood(
    request: MoodAnalysisRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze mood from text and images."""
    return await analysis_service.analyze_user_mood(request, current_user.id, db)

@router.post("/extract-embedding")
async def extract_embedding(
    image_urls: List[str],
    current_user = Depends(get_current_user),
):
    """Extract embeddings from images."""
    return await analysis_service.extract_embeddings(image_urls)
