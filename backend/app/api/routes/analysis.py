"""Analysis routes — Gemini only, no NLP model loading."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger
import json
import re

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
        raise HTTPException(status_code=400, detail="text_description is required")

    logger.info(f"Mood analysis: {request.text_description[:80]}")

    try:
        prompt = (
            'Return ONLY this exact JSON, no explanation, no markdown:\n'
            '{"style":"X","mood":"X","lighting":"X","location_type":"X","edit_style":"X","keywords":["X","X","X"]}\n\n'
            'Fill in X based on this photography request: '
            + request.text_description
        )

        gemini_raw = await gemini_service.generate_content(prompt)

        analysis = {}
        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            found = re.search(r'\{.*\}', clean, re.DOTALL)
            if found:
                analysis = json.loads(found.group())
            else:
                raise ValueError("No JSON found")
        except Exception:
            analysis = {
                "style": "unknown",
                "mood": "unknown",
                "lighting": "",
                "location_type": "",
                "edit_style": "",
                "keywords": [],
            }

        return {
            "status": "success",
            "analysis": analysis,
            "original_text": request.text_description,
        }

    except Exception as e:
        logger.error(f"Mood analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
