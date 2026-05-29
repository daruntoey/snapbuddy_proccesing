"""Analysis routes — Gemini with constrained SnapBuddy vocabulary."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger
import json
import re

from app.ai.gemini_service import gemini_service

router = APIRouter()

# ── SnapBuddy Vocabulary ──────────────────────────────────────────────────────
MOOD_TAGS = [
    "Candid", "Clean Girl", "Cute Cafe", "Film Tone", "Korean Soft",
    "Luxury", "Minimal", "Natural Fresh", "Street Vibe", "Sun-kissed", "Urban Casual",
]
POSE_STYLES = [
    "Action", "Cafe Candid", "Candid", "Elegant", "Lifestyle Pose",
    "Look Away", "Natural Smile", "Posed", "Romantic", "Sitting Pose", "Walking Shot",
]
LOCATION_TYPES = [
    "Cafe", "Indoor", "Mall", "Museum", "Outdoor",
    "Park", "Restaurant", "Rooftop", "Street", "Studio", "Tourist Spot",
]
CATEGORIES = [
    "Cafe Lifestyle", "Cafe Portrait", "Casual Portrait", "Close-up Portrait",
    "Couples", "Evening Vibe", "Event Portrait", "Film Look", "Lifestyle Portrait",
    "Luxury Dining", "Minimalist", "Nature Portrait", "Outdoor Portrait",
    "Street Fashion", "Street Portrait", "Sweet Cafe", "Travel Portrait",
]
LIGHTING_TAGS = [
    "Cloudy Soft Light", "Golden Hour", "Indoor Ambient", "Indoor Soft Light",
    "Morning Light", "Natural Light", "Night Light", "Soft Daylight", "Window Light",
]

EMPTY_ANALYSIS = {
    "mood_tags": [], "pose_styles": [],
    "location_types": [], "categories": [], "lighting_tags": [],
}


def filter_valid(values, allowed: list) -> list:
    if not isinstance(values, list):
        return []
    # Exact match first, then case-insensitive fallback
    result = []
    for v in values:
        if v in allowed:
            result.append(v)
        else:
            # Case-insensitive match
            match = next((a for a in allowed if a.lower() == str(v).lower()), None)
            if match:
                result.append(match)
    return result
# ─────────────────────────────────────────────────────────────────────────────


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
            "Analyze the user's photography request and pick the BEST MATCHING values "
            "ONLY from the provided lists. You may select multiple values per field.\n\n"
            f"User request: \"{request.text_description}\"\n\n"
            "Available values (use EXACT spelling):\n"
            f"mood_tags: {MOOD_TAGS}\n"
            f"pose_styles: {POSE_STYLES}\n"
            f"location_types: {LOCATION_TYPES}\n"
            f"categories: {CATEGORIES}\n"
            f"lighting_tags: {LIGHTING_TAGS}\n\n"
            "Rules:\n"
            "1. Use EXACT values from the lists — do NOT paraphrase or invent new values\n"
            "2. Each field must be a JSON array (can be empty [] if nothing fits)\n"
            "3. Return ONLY the JSON object, no markdown, no explanation\n\n"
            "JSON format:\n"
            '{"mood_tags":[...],"pose_styles":[...],'
            '"location_types":[...],"categories":[...],"lighting_tags":[...]}'
        )

        gemini_raw = await gemini_service.generate_content(prompt)
        logger.info(f"Gemini raw: {gemini_raw[:150]}")

        # Start with safe default — always has all keys
        analysis = dict(EMPTY_ANALYSIS)

        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            found = re.search(r'\{.*\}', clean, re.DOTALL)
            if found:
                raw = json.loads(found.group())
                analysis = {
                    "mood_tags":      filter_valid(raw.get("mood_tags", []),      MOOD_TAGS),
                    "pose_styles":    filter_valid(raw.get("pose_styles", []),    POSE_STYLES),
                    "location_types": filter_valid(raw.get("location_types", []), LOCATION_TYPES),
                    "categories":     filter_valid(raw.get("categories", []),     CATEGORIES),
                    "lighting_tags":  filter_valid(raw.get("lighting_tags", []),  LIGHTING_TAGS),
                }
                logger.info(f"Parsed analysis: {analysis}")
            else:
                logger.warning("No JSON found in Gemini response")
        except Exception as e:
            logger.warning(f"JSON parse failed: {e} | raw: {gemini_raw[:200]}")

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
    """Return all available SnapBuddy tag vocabularies."""
    return {
        "mood_tags": MOOD_TAGS,
        "pose_styles": POSE_STYLES,
        "location_types": LOCATION_TYPES,
        "categories": CATEGORIES,
        "lighting_tags": LIGHTING_TAGS,
    }
