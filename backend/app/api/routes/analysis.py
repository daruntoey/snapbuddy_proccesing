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
            "Available values:\n"
            f"mood_tags: {MOOD_TAGS}\n"
            f"pose_styles: {POSE_STYLES}\n"
            f"location_types: {LOCATION_TYPES}\n"
            f"categories: {CATEGORIES}\n"
            f"lighting_tags: {LIGHTING_TAGS}\n\n"
            "Return ONLY a JSON object with these exact keys. "
            "Each value must be a list of strings chosen STRICTLY from the lists above. "
            "Do not invent new values. Do not include markdown.\n"
            "Example format:\n"
            '{"mood_tags":["Korean Soft","Cute Cafe"],'
            '"pose_styles":["Candid","Natural Smile"],'
            '"location_types":["Cafe"],'
            '"categories":["Cafe Portrait","Cafe Lifestyle"],'
            '"lighting_tags":["Morning Light","Natural Light"]}'
        )

        gemini_raw = await gemini_service.generate_content(prompt)

        # Parse JSON
        analysis = {}
        try:
            clean = re.sub(r"```(?:json)?|```", "", gemini_raw or "").strip()
            found = re.search(r'\{.*\}', clean, re.DOTALL)
            if found:
                raw = json.loads(found.group())
                # Validate — keep only values that exist in our lists
                def filter_valid(values: list, allowed: list) -> list:
                    return [v for v in (values or []) if v in allowed]

                analysis = {
                    "mood_tags":      filter_valid(raw.get("mood_tags", []),      MOOD_TAGS),
                    "pose_styles":    filter_valid(raw.get("pose_styles", []),    POSE_STYLES),
                    "location_types": filter_valid(raw.get("location_types", []), LOCATION_TYPES),
                    "categories":     filter_valid(raw.get("categories", []),     CATEGORIES),
                    "lighting_tags":  filter_valid(raw.get("lighting_tags", []),  LIGHTING_TAGS),
                }
        except Exception as e:
            logger.warning(f"JSON parse failed: {e}")
            analysis = {
                "mood_tags": [], "pose_styles": [],
                "location_types": [], "categories": [], "lighting_tags": [],
            }

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
