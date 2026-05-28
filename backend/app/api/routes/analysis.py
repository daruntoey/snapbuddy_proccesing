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
            "Analyze this photography request and return a JSON object.\n"
            "Request: " + request.text_description + "\n\n"
            "Return JSON with these keys: style, mood, lighting, location_type, edit_style, keywords (array).\n"
            "Return ONLY the JSON object, no other text."
        )

        gemini_raw = await gemini_service.generate_content(prompt)

        raw_data = {}
        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            found = re.search(r'\{.*\}', clean, re.DOTALL)
            if found:
                raw_data = json.loads(found.group())
        except Exception:
            pass

        # remap — รับ field ชื่ออะไรก็ได้จาก Gemini แล้วแปลงให้ตรง
        def pick(d, *keys):
            for k in keys:
                for dk in d:
                    if k.lower() in dk.lower():
                        return d[dk]
            return ""

        def pick_list(d, *keys):
            for k in keys:
                for dk in d:
                    if k.lower() in dk.lower():
                        v = d[dk]
                        if isinstance(v, list):
                            return v
                        if isinstance(v, str):
                            return [x.strip() for x in v.split(",")]
            return []

        analysis = {
            "style":         pick(raw_data, "style", "aesthetic"),
            "mood":          pick(raw_data, "mood", "feeling", "atmosphere"),
            "lighting":      pick(raw_data, "lighting", "light"),
            "location_type": pick(raw_data, "location", "place", "venue"),
            "edit_style":    pick(raw_data, "edit", "tone", "color", "grade"),
            "keywords":      pick_list(raw_data, "keyword", "tag", "element", "recommend"),
        }

        # fallback ถ้า Gemini ไม่คืน JSON เลย
        if not analysis["style"]:
            analysis["style"] = request.text_description[:60]

        return {
            "status": "success",
            "analysis": analysis,
            "original_text": request.text_description,
        }

    except Exception as e:
        logger.error(f"Mood analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
