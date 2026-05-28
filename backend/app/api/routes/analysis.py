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

    try:
        prompt = (
            "You are a photography assistant. Analyze this request: "
            + request.text_description
            + "\n\nReturn ONLY a JSON object with these exact keys and no other text:\n"
            + '{"style":"...","mood":"...","lighting":"...","location_type":"...","edit_style":"...","keywords":["...","...","..."]}'
        )

        gemini_raw = await gemini_service.generate_content(prompt)

        # Parse whatever Gemini returns
        raw = {}
        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            found = re.search(r'\{.*\}', clean, re.DOTALL)
            if found:
                raw = json.loads(found.group())
        except Exception:
            pass

        # Helper: find value by partial key match
        def get(d, *keys, default=""):
            for key in keys:
                for k, v in d.items():
                    if key.lower() in k.lower() and isinstance(v, str):
                        return v
            return default

        def get_list(d, *keys):
            for key in keys:
                for k, v in d.items():
                    if key.lower() in k.lower():
                        if isinstance(v, list):
                            return [str(x) for x in v]
                        if isinstance(v, str):
                            return [x.strip() for x in v.split(",") if x.strip()]
            return []

        # Extract lighting from elements/recommendations if missing
        lighting = get(raw, "lighting", "light")
        if not lighting:
            elements = get_list(raw, "element", "recommend", "keyword")
            lighting = next((e for e in elements if "light" in e.lower()), "")

        analysis = {
            "style":         get(raw, "style", "aesthetic", "type"),
            "mood":          get(raw, "mood", "feeling", "atmosphere", "vibe"),
            "lighting":      lighting,
            "location_type": get(raw, "location", "place", "setting", "venue"),
            "edit_style":    get(raw, "edit", "tone", "color", "grade", "processing"),
            "keywords":      get_list(raw, "keyword", "tag", "element", "recommend"),
        }

        # Fallback for style
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
