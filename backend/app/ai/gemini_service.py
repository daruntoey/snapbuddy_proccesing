"""Gemini service — requests + asyncio.to_thread, thinking disabled."""
import asyncio
import json
import os
import requests
from loguru import logger


class GeminiService:
    # Confirmed working models from /debug/gemini-models
    ENDPOINTS = [
        ("v1beta", "gemini-2.5-flash"),
        ("v1beta", "gemini-flash-latest"),
        ("v1beta", "gemini-2.5-flash-lite"),
        ("v1beta", "gemini-1.5-flash"),
    ]
    BASE = "https://generativelanguage.googleapis.com"

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.working_endpoint = None  # cached (version, model) tuple
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - will use mock")
        else:
            logger.info(f"GeminiService ready, key_length={len(self.api_key)}")

    def _build_payload(self, prompt: str) -> dict:
        return {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
                # Disable thinking to prevent token budget consumption
                "thinkingConfig": {"thinkingBudget": 0},
            },
        }

    def _sync_call(self, version: str, model: str, prompt: str) -> dict:
        url = f"{self.BASE}/{version}/models/{model}:generateContent"
        resp = requests.post(
            f"{url}?key={self.api_key}",
            json=self._build_payload(prompt),
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        return {"status": resp.status_code, "body": resp.text, "model": model}

    def _extract_text(self, body: str) -> str:
        """Extract text from Gemini response, skipping thinking parts."""
        data = json.loads(body)
        parts = data["candidates"][0]["content"]["parts"]
        # Skip thinking parts (thought: true), get actual response
        for part in parts:
            if not part.get("thought", False) and "text" in part:
                return part["text"]
        # Fallback: return first text part
        return parts[0].get("text", "")

    async def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            return self._mock()

        endpoints = (
            [self.working_endpoint] if self.working_endpoint
            else self.ENDPOINTS
        )

        for version, model in endpoints:
            logger.info(f"Trying: {model} ({version})")
            try:
                result = await asyncio.to_thread(
                    self._sync_call, version, model, prompt
                )
                status = result["status"]
                body = result["body"]
                logger.info(f"HTTP {status} from {model}")

                if status == 200:
                    text = self._extract_text(body)
                    logger.info(f"Gemini OK ({model}): '{text[:100]}'")
                    self.working_endpoint = (version, model)
                    return text

                if status in (400, 404, 429):
                    logger.warning(f"{model} returned {status}, trying next...")
                    continue

                logger.error(f"Gemini {status} from {model}: {body[:200]}")
                continue

            except requests.exceptions.Timeout:
                logger.error(f"{model} timed out")
                continue
            except Exception as e:
                logger.error(f"{model} error: {type(e).__name__}: {e}")
                continue

        logger.error("All Gemini models failed - returning mock")
        return self._mock()

    def _mock(self) -> str:
        return json.dumps({
            "mood_tags": [], "pose_styles": [],
            "location_types": [], "categories": [], "lighting_tags": [],
        })


gemini_service = GeminiService()
