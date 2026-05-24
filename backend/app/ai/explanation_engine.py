"""AI explanation generation using Gemini."""
from typing import Dict
from app.ai.gemini_service import gemini_service


class ExplanationEngine:
    """Generate natural language explanations for matches."""

    async def generate_explanation(
        self,
        photographer_data: Dict,
        user_preferences: Dict,
        scores: Dict,
    ) -> str:
        """Generate match explanation."""
        return await gemini_service.generate_match_explanation(
            photographer_info=photographer_data,
            user_aesthetic=user_preferences,
            match_score=scores.get("match_score", 0),
        )


explanation_engine = ExplanationEngine()
