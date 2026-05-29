"""Analysis routes — Gemini with constrained SnapBuddy vocabulary."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger
import json
import re

from app.ai.gemini_service import gemini_service

router = APIRouter()

MOOD_TAGS = ["Candid","Clean Girl","Cute Cafe","Film Tone","Korean Soft","Luxury","Minimal","Natural Fresh","Street Vibe","Sun-kissed","Urban Casual"]
POSE_STYLES = ["Action","Cafe Candid","Candid","Elegant","Lifestyle Pose","Look Away","Natural Smile","Posed","Romantic","Sitting Pose","Walking Shot"]
LOCATION_TYPES = ["Cafe","Indoor","Mall","Museum","Outdoor","Park","Restaurant","Rooftop","Street","Studio","Tourist Spot"]
CATEGORIES = ["Cafe Lifestyle","Cafe Portrait","Casual Portrait","Close-up Portrait","Couples","Evening Vibe","Event Portrait","Film Look","Lifestyle Portrait","Luxury Dining","Minimalist","Nature Portrait","Outdoor Portrait","Street Fashion","Street Portrait","Sweet Cafe","Travel Portrait"]
LIGHTING_TAGS = ["Cloudy Soft Light","Golden Hour","Indoor Ambient","Indoor Soft Light","Morning Light","Natural Light","Night Light","Soft Daylight","Window Light"]

EMPTY_ANALYSIS = {"mood_tags":[],"pose_styles":[],"location_types":[],"categories":[],"lighting_tags":[]}


def filter_valid(values, allowed: list) -> list:
    if not isinstance(values, list):
        return []
    result = []
    for v in values:
        if v in allowed:
            result.append(v)
        else:
            # case-insensitive fallback
            m = next((a for a in allowed if a.lower() == str(v).lower()), None)
            if m:
                result.append(m)
    return result


def parse_gemini_json(raw: str) -> dict:
    """Try multiple strategies to extract JSON from Gemini response."""
    if not raw:
        return {}

    # Strategy 1: direct parse
    try:
        return json.loads(raw.strip())
    except Exception:
        pass

    # Strategy 2: remove markdown fences then parse
    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Strategy 3: find first { to last } (handles extra text around JSON)
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw[start:end+1])
        except Exception:
            pass

    return {}


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
            "You are a SnapBuddy photography assistant. "
            "Analyze the request and pick BEST MATCHING values ONLY from the lists.\n\n"
            f"Request: \"{request.text_description}\"\n\n"
            f"mood_tags: {MOOD_TAGS}\n"
            f"pose_styles: {POSE_STYLES}\n"
            f"location_types: {LOCATION_TYPES}\n"
            f"categories: {CATEGORIES}\n"
            f"lighting_tags: {LIGHTING_TAGS}\n\n"
            "Use EXACT spelling. Return ONLY this JSON (no markdown):\n"
            '{"mood_tags":[...],"pose_styles":[...],"location_types":[...],"categories":[...],"lighting_tags":[...]}'
        )

        gemini_raw = await gemini_service.generate_content(prompt)
        logger.info(f"Gemini full response: {gemini_raw}")

        # Always start with safe default
        analysis = dict(EMPTY_ANALYSIS)

        raw_dict = parse_gemini_json(gemini_raw)
        logger.info(f"Parsed dict: {raw_dict}")

        if raw_dict:
            analysis = {
                "mood_tags":      filter_valid(raw_dict.get("mood_tags", []),      MOOD_TAGS),
                "pose_styles":    filter_valid(raw_dict.get("pose_styles", []),    POSE_STYLES),
                "location_types": filter_valid(raw_dict.get("location_types", []), LOCATION_TYPES),
                "categories":     filter_valid(raw_dict.get("categories", []),     CATEGORIES),
                "lighting_tags":  filter_valid(raw_dict.get("lighting_tags", []),  LIGHTING_TAGS),
            }
            logger.info(f"Final analysis: {analysis}")
        else:
            logger.warning(f"Could not parse JSON from: {gemini_raw[:300]}")

        return {
            "status": "success",
            "analysis": analysis,
            "original_text": request.text_description,
        }

    except Exception as e:
        logger.error(f"Mood analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vocabulary")
async def get_vocabulary():
    return {
        "mood_tags": MOOD_TAGS,
        "pose_styles": POSE_STYLES,
        "location_types": LOCATION_TYPES,
        "categories": CATEGORIES,
        "lighting_tags": LIGHTING_TAGS,
    }
