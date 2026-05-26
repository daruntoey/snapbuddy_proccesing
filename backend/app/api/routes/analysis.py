"""AI analysis routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.analysis import MoodAnalysisRequest, MoodAnalysisResponse
from app.services.analysis_service import analysis_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/mood")
async def analyze_mood(
    request: MoodAnalysisRequest,
):
    """
    Analyze mood from text using AI (No images needed).
    """
    from app.ai.gemini_service import gemini_service
    from app.ai.nlp_service import nlp_service
    
    try:
        # 1. Analyze text with NLP
        text_embedding = None
        if request.text_description:
            text_embedding = await nlp_service.extract_text_embedding(
                request.text_description
            )
        
        # 2. Generate mood analysis with Gemini (ไม่ต้องรูป)
        prompt = f"""
        Analyze this photography aesthetic request:
        
        Description: {request.text_description or "No description"}
        Budget: ${request.budget_min} - ${request.budget_max}
        Location: {request.location or "Not specified"}
        
        Provide detailed analysis in JSON format with keys:
        - style: Photography style preference
        - mood: Mood and atmosphere
        - recommendations: Photographer characteristics needed
        - elements: Key aesthetic elements
        
        Return ONLY valid JSON, no markdown.
        """
        
        analysis_text = await gemini_service.generate_content(prompt)
        
        # Parse JSON
        import json
        try:
            analysis = json.loads(analysis_text)
        except:
            analysis = {
                "style": "Professional aesthetic",
                "mood": "Clean and professional",
                "recommendations": "Experienced photographer with portfolio",
                "elements": ["professional lighting", "clean composition"]
            }
        
        return {
            "mood_spec_id": 1,
            "analysis": analysis,
            "text_embedding": text_embedding.tolist() if text_embedding is not None else None,
        }
        
    except Exception as e:
        logger.error(f"Mood analysis failed: {e}")
        raise HTTPException(500, f"Analysis failed: {str(e)}")
