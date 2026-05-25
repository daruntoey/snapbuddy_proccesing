"""NLP service for mood and text analysis."""
from typing import Dict, List
import numpy as np
from loguru import logger

from app.config import settings


class NLPMoodAnalyzer:
    """NLP service for analyzing mood from text."""

    def __init__(self):
        self.model = None
        logger.info("NLP Service initialized (lazy loading enabled)")

    def _load_model(self):
        """Load model only when needed."""
        if self.model is None:
            logger.info("Loading Sentence Transformer model on first use...")
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
            logger.info("Sentence Transformer model loaded successfully")

    async def extract_text_embedding(self, text: str) -> np.ndarray:
        """Extract sentence embedding from text."""
        try:
            self._load_model()
            embedding = self.model.encode(text, normalize_embeddings=True)
            return embedding
        except Exception as e:
            logger.error(f"Failed to extract text embedding: {e}")
            # Return dummy embedding if fails
            return np.random.rand(384).astype(np.float32)

    async def extract_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Extract embeddings for multiple texts."""
        try:
            self._load_model()
            embeddings = self.model.encode(texts, normalize_embeddings=True, batch_size=32)
            return embeddings
        except Exception as e:
            logger.error(f"Failed to extract batch embeddings: {e}")
            # Return dummy embeddings if fails
            return np.random.rand(len(texts), 384).astype(np.float32)


nlp_service = NLPMoodAnalyzer()
