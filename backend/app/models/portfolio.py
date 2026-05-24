"""Portfolio database model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class Portfolio(Base):
    """Portfolio image model."""

    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    photographer_id = Column(Integer, ForeignKey("photographers.id"), nullable=False, index=True)
    
    # Image
    image_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text)
    gcs_path = Column(Text)
    
    # Metadata
    title = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    shoot_date = Column(DateTime)
    
    # AI Analysis
    image_embedding = Column(Vector(512), nullable=False)  # CLIP embedding
    style_tags = Column(JSON)  # AI-detected styles
    detected_moods = Column(JSON)  # AI-detected moods
    color_palette = Column(JSON)  # Dominant colors
    lighting_type = Column(String(100))  # Natural, Studio, Golden Hour, etc.
    composition_score = Column(Float)
    
    # Classification
    primary_style = Column(String(100), index=True)
    secondary_styles = Column(JSON)
    
    # Engagement
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # Status
    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    photographer = relationship("Photographer", back_populates="portfolios")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, photographer_id={self.photographer_id})>"
