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
            # ลอง model name ที่รองรับใน version 0.3.2
            for model_name in ["gemini-1.0-pro", "gemini-pro"]:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    logger.info(f"Gemini ready: {model_name}")
                    break
                except Exception:
                    continue
            if not self.model:
                logger.error("No Gemini model available")
        except Exception as e:
            logger.error(f"Gemini init failed: {e}")

    async def generate_content(self, prompt: str) -> str:
        if not self.model:
            logger.warning("Gemini not available - using mock")
            return self._mock()
        try:
            logger.info(f"Calling Gemini... prompt length={len(prompt)}")

            def _call():
                resp = self.model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.3, "max_output_tokens": 500},
                )
                return resp.text

            result = await asyncio.wait_for(
                asyncio.to_thread(_call),
                timeout=25.0,
            )
            logger.info(f"Gemini OK: {result[:80]}")
            return result
        except asyncio.TimeoutError:
            logger.error("Gemini timeout after 25s")
            return self._mock()
        except Exception as e:
            logger.error(f"Gemini error: {type(e).__name__}: {e}")
            return self._mock()

    def _mock(self) -> str:
        return json.dumps({
            "style": "mock", "mood": "mock",
            "lighting": "", "location_type": "",
            "edit_style": "", "keywords": [],
        })


gemini_service = GeminiService()
