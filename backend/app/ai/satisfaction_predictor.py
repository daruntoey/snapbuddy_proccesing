"""ML-based satisfaction prediction."""
from typing import Dict
import math


class SatisfactionPredictor:
    """Predict booking satisfaction probability."""

    def predict_satisfaction(
        self,
        match_score: float,
        photographer_rating: float,
        photographer_reviews: int,
        price_ratio: float,
    ) -> float:
        """
        Predict satisfaction probability (0-1).
        
        Simple heuristic model (can be replaced with trained ML model).
        """
        # Normalize inputs
        score_factor = match_score / 100.0
        rating_factor = photographer_rating / 5.0
        
        # Reviews confidence (more reviews = more confidence)
        review_confidence = min(1.0, photographer_reviews / 20.0)
        
        # Price acceptance (1.0 if within budget, lower if higher)
        price_factor = max(0.5, 1.0 - max(0, price_ratio - 1.0) * 0.5)
        
        # Weighted combination
        satisfaction = (
            0.40 * score_factor +
            0.30 * rating_factor +
            0.15 * review_confidence +
            0.15 * price_factor
        )
        
        return round(satisfaction, 3)


satisfaction_predictor = SatisfactionPredictor()
