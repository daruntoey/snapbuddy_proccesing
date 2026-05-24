"""Computer vision service for image analysis and embedding extraction."""
import io
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from loguru import logger

from app.config import settings


class ComputerVisionService:
    """Service for image analysis using CLIP."""

    def __init__(self):
        """Initialize CV service with CLIP model."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing CLIP on device: {self.device}")
        
        # Load CLIP model
        self.model = CLIPModel.from_pretrained(settings.CLIP_MODEL_NAME)
        self.processor = CLIPProcessor.from_pretrained(settings.CLIP_MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()
        
        # Style classification keywords
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

    async def extract_image_embedding(
        self,
        image_bytes: bytes,
    ) -> np.ndarray:
        """
        Extract CLIP embedding from image bytes.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            512-dimensional embedding vector
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            # Process image
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Extract features
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
                # Normalize
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Convert to numpy
            embedding = image_features.cpu().numpy()[0]
            
            return embedding
        except Exception as e:
            logger.error(f"Failed to extract image embedding: {e}")
            raise

    async def classify_image_style(
        self,
        image_bytes: bytes,
    ) -> Dict[str, float]:
        """
        Classify image style using zero-shot CLIP classification.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dict of style labels to confidence scores
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            # Process image and text
            inputs = self.processor(
                text=self.style_keywords,
                images=image,
                return_tensors="pt",
                padding=True,
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
            
            # Convert to dict
            probs_np = probs.cpu().numpy()[0]
            style_scores = {
                style: float(score)
                for style, score in zip(self.style_keywords, probs_np)
            }
            
            # Sort by score
            style_scores = dict(
                sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
            )
            
            return style_scores
        except Exception as e:
            logger.error(f"Failed to classify image style: {e}")
            raise

    async def detect_lighting_type(
        self,
        image_bytes: bytes,
    ) -> str:
        """
        Detect lighting type in image.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Detected lighting type
        """
        lighting_types = [
            "natural light",
            "golden hour lighting",
            "studio lighting",
            "low key dark lighting",
            "high key bright lighting",
            "window light",
            "artificial indoor lighting",
        ]
        
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            inputs = self.processor(
                text=lighting_types,
                images=image,
                return_tensors="pt",
                padding=True,
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
            
            # Get top prediction
            top_idx = probs.argmax().item()
            return lighting_types[top_idx]
        except Exception as e:
            logger.error(f"Failed to detect lighting type: {e}")
            return "unknown"

    async def extract_color_palette(
        self,
        image_bytes: bytes,
        num_colors: int = 5,
    ) -> List[str]:
        """
        Extract dominant color palette from image.
        
        Args:
            image_bytes: Raw image bytes
            num_colors: Number of dominant colors to extract
            
        Returns:
            List of hex color codes
        """
        try:
            from sklearn.cluster import KMeans
            
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image = image.resize((150, 150))  # Reduce size for performance
            
            # Convert to array
            pixels = np.array(image).reshape(-1, 3)
            
            # Cluster colors
            kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get cluster centers (dominant colors)
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert to hex
            hex_colors = [
                f"#{r:02x}{g:02x}{b:02x}" for r, g, b in colors
            ]
            
            return hex_colors
        except Exception as e:
            logger.error(f"Failed to extract color palette: {e}")
            return []

    async def analyze_image_comprehensive(
        self,
        image_bytes: bytes,
    ) -> Dict[str, any]:
        """
        Comprehensive image analysis.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dict with embedding, styles, lighting, colors
        """
        try:
            # Extract all features
            embedding = await self.extract_image_embedding(image_bytes)
            style_scores = await self.classify_image_style(image_bytes)
            lighting = await self.detect_lighting_type(image_bytes)
            colors = await self.extract_color_palette(image_bytes)
            
            # Get top styles
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

    async def compute_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score (0-1)
        """
        # Ensure numpy arrays
        if isinstance(embedding1, list):
            embedding1 = np.array(embedding1)
        if isinstance(embedding2, list):
            embedding2 = np.array(embedding2)
        
        # Normalize
        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)
        
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2)
        
        return float(similarity)


# Global instance
cv_service = ComputerVisionService()
