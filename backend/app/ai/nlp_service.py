"""NLP service for mood and text analysis."""
from typing import Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger

from app.config import settings


class NLPMoodAnalyzer:
    """NLP service for analyzing mood from text."""

    def __init__(self):
        self.model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

    async def extract_text_embedding(self, text: str) -> np.ndarray:
        """Extract sentence embedding from text."""
        try:
            embedding = self.model.encode(text, normalize_embeddings=True)
            return embedding
        except Exception as e:
            logger.error(f"Failed to extract text embedding: {e}")
            raise

    async def extract_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Extract embeddings for multiple texts."""
        try:
            embeddings = self.model.encode(texts, normalize_embeddings=True, batch_size=32)
            return embeddings
        except Exception as e:
            logger.error(f"Failed to extract batch embeddings: {e}")
            raise


nlp_service = NLPMoodAnalyzer()
