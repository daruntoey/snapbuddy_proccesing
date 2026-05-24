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
