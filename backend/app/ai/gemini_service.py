"""Gemini service for AI content generation."""
from google import generativeai as genai
from loguru import logger
import asyncio
import os


class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found - using mock")
            self.model = None
            return
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini model initialized")
        except Exception as e:
            logger.error(f"Failed to init Gemini: {e}")
            self.model = None

    async def generate_content(self, prompt: str) -> str:
        try:
            if not self.model:
                return self._mock(prompt)

            # run sync SDK in thread to avoid blocking event loop
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return response.text

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return self._mock(prompt)

    def _mock(self, prompt: str) -> str:
        import json
        return json.dumps({
            "style": "mock",
            "mood": "mock",
            "lighting": "",
            "location_type": "",
            "edit_style": "",
            "keywords": []
        })


gemini_service = GeminiService()
