"""Gemini service — requests + asyncio.to_thread."""
import asyncio
import json
import os
import requests
from loguru import logger


class GeminiService:
    # gemini-2.5-flash is confirmed working from /debug/gemini-models
    ENDPOINTS = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview:generateContent",
    ]

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.working_url: str | None = None
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - will use mock")
        else:
            logger.info(f"GeminiService ready, key_length={len(self.api_key)}")

    def _sync_call(self, url: str, prompt: str) -> dict:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
            },
        }
        resp = requests.post(
            f"{url}?key={self.api_key}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
            verify=True,
        )
        return {"status": resp.status_code, "body": resp.text}

    async def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            return self._mock()

        urls = [self.working_url] if self.working_url else self.ENDPOINTS

        for url in urls:
            model = url.split("/models/")[-1].split(":")[0]
            logger.info(f"Trying: {model}")
            try:
                result = await asyncio.to_thread(self._sync_call, url, prompt)
                status = result["status"]
                body = result["body"]
                logger.info(f"HTTP {status} from {model}")

                if status == 200:
                    data = json.loads(body)
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    logger.info(f"Gemini OK ({model}): '{text[:80]}'")
                    self.working_url = url
                    return text

                if status in (400, 404):
                    logger.warning(f"{model} returned {status}, trying next...")
                    continue

                if status == 429:
                    logger.warning(f"{model} rate limited, trying next...")
                    continue

                logger.error(f"Gemini {status} from {model}: {body[:200]}")
                continue

            except requests.exceptions.Timeout:
                logger.error(f"{model} timed out")
                continue
            except requests.exceptions.ConnectionError as e:
                logger.error(f"{model} connection error: {e}")
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
