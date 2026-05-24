"""Gemini API service for AI-powered explanations and analysis."""
import json
from typing import Any, Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

import google.generativeai as genai
from loguru import logger

from app.config import settings


class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini service."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    @retry(
        stop=stop_after_attempt(settings.GEMINI_MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            config = self.generation_config.copy()
            config["temperature"] = temperature
            config["max_output_tokens"] = max_tokens

            response = await self.model.generate_content_async(
                prompt,
                generation_config=config,
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    @retry(
        stop=stop_after_attempt(settings.GEMINI_MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate_structured_json(
        self,
        prompt: str,
        schema: Dict[str, Any],
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output using Gemini.
        
        Args:
            prompt: Input prompt with JSON schema instructions
            schema: Expected JSON schema
            temperature: Lower for more deterministic output
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            full_prompt = f"""{prompt}

Return ONLY a valid JSON object matching this schema:
{json.dumps(schema, indent=2)}

Do not include any explanation, markdown formatting, or code blocks. Return only the raw JSON.
"""
            
            config = self.generation_config.copy()
            config["temperature"] = temperature
            config["max_output_tokens"] = 2048

            response = await self.model.generate_content_async(
                full_prompt,
                generation_config=config,
            )
            
            # Parse JSON response
            text = response.text.strip()
            # Remove potential markdown code blocks
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini: {e}")
            logger.error(f"Response text: {response.text}")
            raise
        except Exception as e:
            logger.error(f"Gemini structured output error: {e}")
            raise

    async def generate_match_explanation(
        self,
        photographer_info: Dict[str, Any],
        user_aesthetic: Dict[str, Any],
        match_score: float,
    ) -> str:
        """
        Generate natural language explanation for photographer match.
        
        Args:
            photographer_info: Photographer profile and portfolio data
            user_aesthetic: User's aesthetic preferences and requirements
            match_score: Calculated match score
            
        Returns:
            Human-readable explanation
        """
        prompt = f"""You are an AI photography matchmaking assistant. Explain why this photographer is a good match for the user's aesthetic preferences.

User's Aesthetic Preferences:
- Mood/Style: {user_aesthetic.get('mood_tags', [])}
- Style Tags: {user_aesthetic.get('style_tags', [])}
- Description: {user_aesthetic.get('description', 'N/A')}
- Budget: ${user_aesthetic.get('budget_min', 0)}-${user_aesthetic.get('budget_max', 0)}
- Location: {user_aesthetic.get('location', 'N/A')}

Photographer Profile:
- Name: {photographer_info.get('business_name', 'N/A')}
- Styles: {photographer_info.get('primary_styles', [])}
- Rating: {photographer_info.get('average_rating', 0)}/5.0
- Completed Shoots: {photographer_info.get('completed_bookings', 0)}
- Hourly Rate: ${photographer_info.get('hourly_rate', 0)}
- Location: {photographer_info.get('location', 'N/A')}

Match Score: {match_score:.1f}/100

Generate a concise, friendly explanation (2-3 sentences) of why this is a great match. Focus on specific style alignment and relevant experience. Be conversational and helpful.
"""
        
        return await self.generate_text(prompt, temperature=0.7, max_tokens=200)

    async def analyze_mood_from_text(
        self,
        text_description: str,
    ) -> Dict[str, Any]:
        """
        Analyze mood and aesthetic preferences from user's text description.
        
        Args:
            text_description: User's natural language description
            
        Returns:
            Structured mood analysis
        """
        schema = {
            "mood_tags": ["cozy", "minimal", "vibrant"],
            "style_tags": ["cafe aesthetic", "natural light"],
            "lighting_preferences": ["warm", "soft"],
            "location_styles": ["indoor", "cafe"],
            "pose_styles": ["candid", "relaxed"],
            "color_preferences": ["warm tones", "earth tones"],
            "detected_intent": "Looking for cozy cafe photoshoot with warm natural lighting",
        }

        prompt = f"""Analyze this photography mood description and extract aesthetic preferences:

Description: "{text_description}"

Extract the following information and return as JSON:
- mood_tags: Array of mood descriptors (e.g., cozy, minimal, dramatic, playful)
- style_tags: Array of photography styles (e.g., Korean cafe aesthetic, street photography)
- lighting_preferences: Array of lighting types (e.g., natural light, golden hour, studio)
- location_styles: Array of location types (e.g., indoor, outdoor, urban, nature)
- pose_styles: Array of posing styles (e.g., candid, posed, lifestyle)
- color_preferences: Array of color preferences (e.g., warm tones, pastels, moody)
- detected_intent: One sentence summary of what the user is looking for
"""
        
        return await self.generate_structured_json(prompt, schema, temperature=0.3)

    async def generate_aesthetic_summary(
        self,
        mood_spec: Dict[str, Any],
    ) -> str:
        """
        Generate a concise summary of the user's aesthetic specification.
        
        Args:
            mood_spec: Complete mood specification
            
        Returns:
            Readable summary
        """
        prompt = f"""Summarize this aesthetic specification in one engaging sentence:

Mood Tags: {mood_spec.get('mood_tags', [])}
Style Tags: {mood_spec.get('style_tags', [])}
Description: {mood_spec.get('text_description', '')}
Location: {mood_spec.get('preferred_location', 'Flexible')}
Budget: ${mood_spec.get('budget_min', 0)}-${mood_spec.get('budget_max', 0)}

Create a single sentence that captures the essence of what they're looking for.
"""
        
        return await self.generate_text(prompt, temperature=0.7, max_tokens=100)

    async def suggest_poses_and_locations(
        self,
        style_tags: List[str],
        mood_tags: List[str],
    ) -> Dict[str, List[str]]:
        """
        Suggest poses and locations based on style and mood.
        
        Args:
            style_tags: Photography style tags
            mood_tags: Mood descriptors
            
        Returns:
            Dict with pose_suggestions and location_suggestions
        """
        schema = {
            "pose_suggestions": [
                "Sitting by window with coffee",
                "Walking through cafe",
            ],
            "location_suggestions": [
                "Minimalist cafe with natural light",
                "Vintage bookshop cafe",
            ],
        }

        prompt = f"""Based on these aesthetic preferences, suggest specific poses and locations:

Style Tags: {style_tags}
Mood Tags: {mood_tags}

Provide 5 specific pose ideas and 5 location suggestions that would fit this aesthetic perfectly.
"""
        
        return await self.generate_structured_json(prompt, schema, temperature=0.8)


# Global instance
gemini_service = GeminiService()
