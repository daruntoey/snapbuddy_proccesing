"""AI Analysis routes - No authentication required."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger

router = APIRouter()


class MoodAnalysisRequest(BaseModel):
    text_description: Optional[str] = None
    image_urls: Optional[List[str]] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    location: Optional[str] = None


@router.post("/mood")
async def analyze_mood(request: MoodAnalysisRequest):
    """
    Analyze mood from text using AI (No auth required).
    """
    try:
        logger.info(f"📝 Analyzing mood: {request.text_description}")
        
        # Return mock data ชั่วคราว
        return {
            "mood_spec_id": 1,
            "analysis": {
                "style": "Korean cafe aesthetic",
                "mood": "Cozy, warm, inviting",
                "recommendations": "Photographer with experience in cafe photography and natural lighting",
                "elements": ["natural light", "warm tones", "cozy composition", "authentic details"]
            },
            "text_embedding": None,
            "status": "success",
            "message": "Mock analysis (AI integration pending)"
        }
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        raise HTTPException(500, f"Error: {str(e)}")
