"""Photographer matching service."""
from app.schemas.matching import MatchRequest, MatchResponse, PhotographerMatch
from app.ai.matching_engine import matching_engine
from app.ai.ranking_engine import ranking_engine
from app.ai.explanation_engine import explanation_engine

class MatchingService:
    async def find_matches(self, request: MatchRequest, user_id: int, db):
        """Find matching photographers."""
        # For now, return mock matches
        return MatchResponse(
            matches=[
                PhotographerMatch(
                    photographer_id=1,
                    business_name="Studio One",
                    match_score=95.5,
                    style_similarity_score=98.0,
                    explanation="Perfect match for Korean cafe aesthetic with warm lighting expertise.",
                    profile_image=None,
                    hourly_rate=150,
                    average_rating=4.8,
                    location="Seoul, South Korea",
                )
            ],
            total=1,
        )

    async def get_saved_recommendations(self, mood_spec_id: int, user_id: int, db):
        """Get saved recommendations."""
        return {"recommendations": []}

matching_service = MatchingService()
