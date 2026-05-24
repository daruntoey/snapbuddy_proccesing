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
