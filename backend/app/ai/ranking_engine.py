"""Recommendation ranking engine with multi-factor scoring."""
from typing import Dict, List
import math
from loguru import logger

from app.config import settings


class RankingEngine:
    """Multi-factor ranking for photographer recommendations."""

    def calculate_match_score(
        self,
        style_similarity: float,
        performance_metrics: Dict,
        budget_fit: float,
        availability_score: float,
        distance_km: float,
    ) -> Dict[str, float]:
        """
        Calculate comprehensive match score.
        
        Formula:
        40% Style Similarity + 25% Performance + 15% Budget + 10% Availability + 10% Distance
        """
        # Normalize components to 0-100 scale
        style_score = style_similarity * 100
        
        # Performance score from ratings and completion rate
        perf_score = (
            performance_metrics.get("average_rating", 0) / 5.0 * 50 +
            performance_metrics.get("completion_rate", 0) * 50
        )
        
        # Budget fit score
        budget_score = budget_fit * 100
        
        # Availability score
        avail_score = availability_score * 100
        
        # Distance score (closer is better, max 50km)
        dist_score = max(0, 100 - (distance_km / 50.0 * 100))
        
        # Weighted total
        final_score = (
            settings.STYLE_WEIGHT * style_score +
            settings.PERFORMANCE_WEIGHT * perf_score +
            settings.BUDGET_WEIGHT * budget_score +
            settings.AVAILABILITY_WEIGHT * avail_score +
            settings.DISTANCE_WEIGHT * dist_score
        )
        
        return {
            "match_score": round(final_score, 2),
            "style_similarity_score": round(style_score, 2),
            "performance_score": round(perf_score, 2),
            "budget_fit_score": round(budget_score, 2),
            "availability_score": round(avail_score, 2),
            "distance_score": round(dist_score, 2),
        }

    def rank_photographers(
        self,
        candidates: List[Dict],
    ) -> List[Dict]:
        """Rank photographers by match score."""
        ranked = sorted(
            candidates,
            key=lambda x: x.get("match_score", 0),
            reverse=True,
        )
        
        # Add rank position
        for i, photographer in enumerate(ranked, 1):
            photographer["rank_position"] = i
        
        return ranked


ranking_engine = RankingEngine()
