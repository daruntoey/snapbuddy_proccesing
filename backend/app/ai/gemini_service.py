"""Gemini service — direct REST API via httpx, no SDK threading issues."""
import os
import json
import httpx
from loguru import logger


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.url = (
            "https://generativelanguage.googleapis.com"
            "/v1beta/models/gemini-pro:generateContent"
        )
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - will use mock")
        else:
            logger.info("Gemini REST client ready (httpx)")

    async def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            logger.warning("No API key - returning mock")
            return self._mock()

        try:
            logger.info(f"Calling Gemini REST API ({len(prompt)} chars)...")
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.url}?key={self.api_key}",
                    json={
                        "contents": [
                            {"parts": [{"text": prompt}]}
                        ],
                        "generationConfig": {
                            "temperature": 0.3,
                            "maxOutputTokens": 300,
                        },
                    },
                )

            if resp.status_code != 200:
                logger.error(f"Gemini HTTP {resp.status_code}: {resp.text[:200]}")
                return self._mock()

            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            logger.info(f"Gemini OK: '{text[:100]}'")
            return text

        except httpx.TimeoutException:
            logger.error("Gemini request timed out after 30s")
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
