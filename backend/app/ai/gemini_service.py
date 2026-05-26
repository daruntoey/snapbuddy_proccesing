"""Gemini service for AI content generation."""
from google import generativeai as genai
from loguru import logger
import os

class GeminiService:
    def __init__(self):
        """Initialize Gemini client."""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            logger.warning("⚠️ GEMINI_API_KEY not found - using mock responses")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini model initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            self.model = None

    async def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini."""
        try:
            if not self.model:
                logger.warning("⚠️ Gemini model not available, returning mock response")
                return self._get_mock_response(prompt)
            
            logger.info("🤖 Calling Gemini API...")
            response = self.model.generate_content(prompt)
            logger.info("✅ Gemini response received")
            
            return response.text
            
        except Exception as e:
            logger.error(f"❌ Gemini error: {e}")
            return self._get_mock_response(prompt)
    
    def _get_mock_response(self, prompt: str) -> str:
        """Return mock response."""
        import json
        return json.dumps({
            "style": "Professional aesthetic",
            "mood": "Clean and modern",
            "recommendations": "Experienced photographer with portfolio",
            "elements": ["professional lighting", "composition", "editing"]
        })

# Global instance
gemini_service = GeminiService()
