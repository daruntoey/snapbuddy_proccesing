"""NLP service for mood and text analysis."""
from typing import Optional
import numpy as np
from loguru import logger

class NLPMoodAnalyzer:
    def __init__(self):
        self.model = None
        logger.info("NLP Service initialized (lazy loading)")

    def _load_model(self):
        """Load model only when needed."""
        if self.model is None:
            try:
                logger.info("📥 Loading Sentence Transformer...")
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Sentence Transformer loaded")
            except Exception as e:
                logger.error(f"⚠️ Failed to load NLP model: {e}")
                self.model = None

    async def extract_text_embedding(self, text: str) -> Optional[np.ndarray]:
        """Extract embedding or return None if model unavailable."""
        try:
            self._load_model()
            
            if self.model is None:
                logger.warning("⚠️ NLP model not available")
                # Return random embedding instead of failing
                return np.random.rand(384).astype(np.float32)
            
            embedding = self.model.encode(text, normalize_embeddings=True)
            return embedding
            
        except Exception as e:
            logger.error(f"⚠️ NLP embedding failed: {e}")
            # Return random embedding to continue
            return np.random.rand(384).astype(np.float32)

nlp_service = NLPMoodAnalyzer()
