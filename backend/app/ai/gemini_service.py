"""Gemini service for AI content generation."""
import asyncio
import os
import json

from loguru import logger


class GeminiService:
    def __init__(self):
        self.model = None
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set")
            return
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            for model_name in ["gemini-1.0-pro", "gemini-pro"]:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    logger.info(f"Gemini ready: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {e}")
            if not self.model:
                logger.error("No Gemini model available")
        except Exception as e:
            logger.error(f"Gemini init failed: {e}")

    async def generate_content(self, prompt: str) -> str:
        if not self.model:
            logger.warning("Gemini model is None - returning mock")
            return self._mock()
        try:
            logger.info(f"Calling Gemini API... ({len(prompt)} chars)")

            def _call():
                return self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.3,
                        "max_output_tokens": 300,
                    },
                ).text

            result = await asyncio.wait_for(
                asyncio.to_thread(_call),
                timeout=55.0,   # เพิ่มจาก 25 → 55 วินาที
            )
            logger.info(f"Gemini response OK: '{result[:100]}'")
            return result

        except asyncio.TimeoutError:
            logger.error("Gemini TIMEOUT after 55s")
            return self._mock()
        except Exception as e:
            logger.error(f"Gemini FAILED: {type(e).__name__}: {e}")
            return self._mock()

    def _mock(self) -> str:
        return json.dumps({
            "style": "mock", "mood": "mock",
            "lighting": "", "location_type": "",
            "edit_style": "", "keywords": [],
        })


gemini_service = GeminiService()
