"""Analysis routes — Gemini only, no NLP model loading."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger
import json, re

from app.ai.gemini_service import gemini_service

router = APIRouter()


class MoodAnalysisRequest(BaseModel):
    text_description: Optional[str] = None
    image_urls: Optional[List[str]] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    location: Optional[str] = None


@router.post("/mood")
async def analyze_mood(request: MoodAnalysisRequest):
    if not request.text_description:
        raise HTTPException(status_code=400, detail="text_descri
