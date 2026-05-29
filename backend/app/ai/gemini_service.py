"""Gemini service — aiohttp REST API, tries multiple model endpoints."""
import os
import json
import aiohttp
from loguru import logger


class GeminiService:
    # Try newer models first, fall back to older ones
    MODELS = [
        ("v1beta", "gemini-1.5-flash"),
        ("v1beta", "gemini-1.5-pro"),
        ("v1",     "gemini-1.0-pro"),
        ("v1beta", "gemini-pro"),
    ]
    BASE = "https://generativelanguage.googleapis.com"

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.working_url = None   # cached after first success
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - will use mock")
        else:
            logger.info(f"GeminiService init OK, key length={len(self.api_key)}")

    async def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            logger.warning("No API key - mock")
            return self._mock()

        # Use cached URL if we found one that works
        urls = (
            [self.working_url] if self.working_url
            else [
                f"{self.BASE}/{v}/models/{m}:generateContent"
                for v, m in self.MODELS
            ]
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 400,
            },
        }

        timeout = aiohttp.ClientTimeout(total=45)

        for url in urls:
            logger.info(f"Trying Gemini: {url.split('/')[-2]}")
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        f"{url}?key={self.api_key}",
                        json=payload,
                        headers={"Content-Type": "application/json"},
                    ) as resp:
                        body = await resp.text()
                        logger.info(f"HTTP {resp.status} from {url.split('/')[-2]}")

                        if resp.status == 200:
                            data = json.loads(body)
                            text = (
                                data["candidates"][0]["content"]["parts"][0]["text"]
                            )
                            logger.info(f"Gemini OK: '{text[:80]}'")
                            self.working_url = url   # cache it
                            return text

                        if resp.status in (400, 404):
                            logger.warning(f"Model unavailable ({resp.status}): {body[:100]}")
                            continue   # try next model

                        logger.error(f"Gemini error {resp.status}: {body[:150]}")
                        return self._mock()

            except aiohttp.ClientConnectorError as e:
                logger.error(f"Connection failed: {e}")
                return self._mock()
            except aiohttp.ServerTimeoutError:
                logger.error("Gemini timeout (45s)")
                return self._mock()
            except Exception as e:
                logger.error(f"Gemini unexpected: {type(e).__name__}: {e}")
                return self._mock()

        logger.error("All Gemini models failed - returning mock")
        return self._mock()

    def _mock(self) -> str:
        return json.dumps({
            "style": "mock", "mood": "mock",
            "lighting": "", "location_type": "",
            "edit_style": "", "keywords": [],
        })


gemini_service = GeminiService()
