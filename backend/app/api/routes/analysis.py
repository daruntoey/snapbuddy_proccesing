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


@router.post("/mood")  # ✅ ไม่มี authentication
async def analyze_mood(request: MoodAnalysisRequest):
    """
    Analyze mood from text using AI (No auth required).
    """
    try:
        from app.ai.gemini_service import gemini_service
        from app.ai.nlp_service import nlp_service
        
        # 1. Analyze text with NLP
        text_embedding = None
        if request.text_description:
            text_embedding = await nlp_service.extract_text_embedding(
                request.text_description
            )
        
        # 2. Generate mood analysis with Gemini
        prompt = f"""
        Analyze this photography aesthetic request and respond ONLY with valid JSON:
        
        Description: {request.text_description or "No description"}
        Budget: ${request.budget_min or 0} - ${request.budget_max or 10000}
        Location: {request.location or "Not specified"}
        
        Return JSON with these exact keys:
        {{
            "style": "photography style preference",
            "mood": "mood and atmosphere",
            "recommendations": "photographer characteristics needed",
            "elements": ["key", "aesthetic", "elements"]
        }}
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
                "recommendations": "Experienced photographer",
                "elements": ["professional lighting", "composition"]
            }
        
        return {
            "mood_spec_id": 1,
            "analysis": analysis,
            "text_embedding": text_embedding.tolist() if text_embedding is not None else None,
        }
        
    except Exception as e:
        logger.error(f"Mood analysis failed: {e}")
        raise HTTPException(500, f"Analysis failed: {str(e)}")
