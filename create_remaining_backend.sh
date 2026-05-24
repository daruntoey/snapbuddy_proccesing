#!/bin/bash

# Create remaining AI services
cat > backend/app/ai/aesthetic_engine.py << 'EOF'
"""Aesthetic specification engine - merges visual and textual features."""
import numpy as np
from typing import Dict, List, Optional
from loguru import logger


class AestheticSpecEngine:
    """Unified aesthetic specification engine."""

    async def merge_embeddings(
        self,
        image_embeddings: List[np.ndarray],
        text_embedding: Optional[np.ndarray] = None,
        image_weight: float = 0.7,
        text_weight: float = 0.3,
    ) -> np.ndarray:
        """
        Merge image and text embeddings into unified aesthetic embedding.
        
        Args:
            image_embeddings: List of CLIP image embeddings
            text_embedding: Sentence transformer text embedding
            image_weight: Weight for image features
            text_weight: Weight for text features
        
        Returns:
            Merged embedding vector
        """
        try:
            # Average image embeddings
            if image_embeddings:
                avg_image_emb = np.mean(image_embeddings, axis=0)
            else:
                avg_image_emb = None

            # Merge with text if available
            if avg_image_emb is not None and text_embedding is not None:
                # Ensure same dimensionality (pad/project if needed)
                if len(avg_image_emb) != len(text_embedding):
                    # Simple approach: use image embedding dimension
                    target_dim = len(avg_image_emb)
                    if len(text_embedding) < target_dim:
                        text_embedding = np.pad(
                            text_embedding,
                            (0, target_dim - len(text_embedding))
                        )
                    else:
                        text_embedding = text_embedding[:target_dim]
                
                # Weighted combination
                merged = (image_weight * avg_image_emb + 
                         text_weight * text_embedding)
                # Normalize
                merged = merged / np.linalg.norm(merged)
                return merged
            elif avg_image_emb is not None:
                return avg_image_emb / np.linalg.norm(avg_image_emb)
            elif text_embedding is not None:
                return text_embedding / np.linalg.norm(text_embedding)
            else:
                raise ValueError("No embeddings provided")
                
        except Exception as e:
            logger.error(f"Failed to merge embeddings: {e}")
            raise


aesthetic_engine = AestheticSpecEngine()
EOF

# Create matching engine
cat > backend/app/ai/matching_engine.py << 'EOF'
"""Photographer matching engine using vector similarity."""
from typing import Dict, List, Tuple
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from loguru import logger

from app.config import settings


class MatchingEngine:
    """Vector similarity matching for photographers."""

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_connection_url,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure Qdrant collection exists."""
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=512,  # CLIP embedding size
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")

    async def index_photographer(
        self,
        photographer_id: int,
        embedding: np.ndarray,
        metadata: Dict,
    ):
        """Index photographer embedding in Qdrant."""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=photographer_id,
                        vector=embedding.tolist(),
                        payload=metadata,
                    )
                ],
            )
            logger.info(f"Indexed photographer {photographer_id}")
        except Exception as e:
            logger.error(f"Failed to index photographer: {e}")
            raise

    async def search_similar_photographers(
        self,
        query_embedding: np.ndarray,
        limit: int = 20,
        filters: Dict = None,
    ) -> List[Tuple[int, float, Dict]]:
        """
        Search for similar photographers.
        
        Returns:
            List of (photographer_id, similarity_score, metadata)
        """
        try:
            # Build filters
            query_filter = None
            if filters:
                conditions = []
                if "budget_max" in filters:
                    conditions.append(
                        FieldCondition(
                            key="hourly_rate",
                            range={"lte": filters["budget_max"]},
                        )
                    )
                if conditions:
                    query_filter = Filter(must=conditions)

            # Search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                query_filter=query_filter,
                limit=limit,
            )

            # Format results
            matches = [
                (result.id, result.score, result.payload)
                for result in results
            ]

            return matches
        except Exception as e:
            logger.error(f"Failed to search photographers: {e}")
            raise


matching_engine = MatchingEngine()
EOF

# Create ranking engine
cat > backend/app/ai/ranking_engine.py << 'EOF'
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
EOF

# Create satisfaction predictor
cat > backend/app/ai/satisfaction_predictor.py << 'EOF'
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
EOF

# Create explanation engine
cat > backend/app/ai/explanation_engine.py << 'EOF'
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
EOF

echo "Remaining AI services created successfully"
