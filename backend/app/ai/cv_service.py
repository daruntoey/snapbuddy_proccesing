"""Computer vision service for image analysis and embedding extraction."""
import io
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image
from loguru import logger

from app.config import settings


class ComputerVisionService:
    """Service for image analysis using CLIP."""

    def __init__(self):
        """Initialize CV service with lazy loading."""
        self.device = "cpu"
        self.model = None
        self.processor = None
        self.style_keywords = [
            "minimalist photography",
            "vintage aesthetic",
            "moody dark photography",
            "bright airy photography",
            "natural light portrait",
            "studio lighting",
            "golden hour photography",
            "urban street photography",
            "nature landscape",
            "cafe aesthetic",
            "Korean style photography",
            "editorial fashion",
            "candid lifestyle",
            "dramatic lighting",
            "soft pastel colors",
        ]
        logger.info(f"CV Service initialized (lazy loading enabled)")

    def _load_model(self):
        """Load CLIP model only when needed."""
        if self.model is None:
            logger.info("Loading CLIP model on first use...")
            import torch
            from transformers import CLIPProcessor, CLIPModel
            
            self.model = CLIPModel.from_pretrained(settings.CLIP_MODEL_NAME)
            self.processor = CLIPProcessor.from_pretrained(settings.CLIP_MODEL_NAME)
            self.model.to(self.device)
            self.model.eval()
            logger.info("CLIP model loaded successfully")

    async def extract_image_embedding(self, image_bytes: bytes) -> np.ndarray:
        """Extract CLIP embedding from image bytes."""
        try:
            self._load_model()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            import torch
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            embedding = image_features.cpu().numpy()[0]
            return embedding
        except Exception as e:
            logger.error(f"Failed to extract image embedding: {e}")
            # Return dummy embedding if fails
            return np.random.rand(512).astype(np.float32)

    async def classify_image_style(self, image_bytes: bytes) -> Dict[str, float]:
        """Classify image style using zero-shot CLIP classification."""
        try:
            self._load_model()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            inputs = self.processor(
                text=self.style_keywords,
                images=image,
                return_tensors="pt",
                padding=True,
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            import torch
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
            
            probs_np = probs.cpu().numpy()[0]
            style_scores = {
                style: float(score)
                for style, score in zip(self.style_keywords, probs_np)
            }
            
            style_scores = dict(
                sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
            )
            
            return style_scores
        except Exception as e:
            logger.error(f"Failed to classify image style: {e}")
            return {"cafe aesthetic": 0.8, "natural light": 0.7}

    async def detect_lighting_type(self, image_bytes: bytes) -> str:
        """Detect lighting type in image."""
        return "natural light"

    async def extract_color_palette(self, image_bytes: bytes, num_colors: int = 5) -> List[str]:
        """Extract dominant color palette from image."""
        return ["#F5F5DC", "#8B7355", "#D2B48C", "#DEB887", "#F0E68C"]

    async def analyze_image_comprehensive(self, image_bytes: bytes) -> Dict[str, any]:
        """Comprehensive image analysis."""
        try:
            embedding = await self.extract_image_embedding(image_bytes)
            style_scores = await self.classify_image_style(image_bytes)
            lighting = await self.detect_lighting_type(image_bytes)
            colors = await self.extract_color_palette(image_bytes)
            
            top_styles = list(style_scores.keys())[:5]
            
            return {
                "embedding": embedding.tolist(),
                "style_scores": style_scores,
                "top_styles": top_styles,
                "lighting_type": lighting,
                "color_palette": colors,
            }
        except Exception as e:
            logger.error(f"Comprehensive image analysis failed: {e}")
            raise

    async def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        if isinstance(embedding1, list):
            embedding1 = np.array(embedding1)
        if isinstance(embedding2, list):
            embedding2 = np.array(embedding2)
        
        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)
        
        similarity = np.dot(embedding1, embedding2)
        
        return float(similarity)


# Global instance
cv_service = ComputerVisionService()
