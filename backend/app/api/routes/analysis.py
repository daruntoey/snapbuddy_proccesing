"""Analysis routes — real NLP mood analysis."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger

from app.ai.nlp_service import nlp_service
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
    """
    Analyse the user's mood/style description.
    - Extracts NLP embedding
    - Uses Gemini to interpret style preferences
    """
    if not request.text_description:
        raise HTTPException(status_code=400, detail="text_description is required")

    logger.info(f"📝 Mood analysis: '{request.text_description[:80]}'")

    try:
        # Get NLP embedding (used internally for matching later)
        embedding = await nlp_service.extract_text_embedding(request.text_description)

        # Use Gemini to parse style keywords
        prompt = f"""วิเคราะห์ความต้องการช่างภาพจาก: "{request.text_description}"

ตอบ JSON เท่านั้น (ไม่ต้องมี markdown):
{{
  "style": "สไตล์หลักที่ต้องการ (1 คำ/วลี)",
  "mood": "อารมณ์ภาพ",
  "lighting": "แสงที่ต้องการ",
  "location_type": "ประเภทสถานที่",
  "edit_style": "สไตล์ตกแต่งภาพ",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

        gemini_raw = await gemini_service.generate_content(prompt)

        import json, re
        analysis = {}
        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            analysis = json.loads(clean)
        except Exception:
            analysis = {
                "style": request.text_description[:50],
                "mood": "ไม่สามารถวิเคราะห์ได้",
                "keywords": [],
            }

        return {
            "status": "success",
            "analysis": analysis,
            "embedding_ready": embedding is not None,
            "original_text": request.text_description,
        }

    except Exception as e:
        logger.error(f"Mood analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
