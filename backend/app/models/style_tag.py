"""Style tag database model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Float

from app.database import Base


class StyleTag(Base):
    """Style tag model for categorizing photography styles."""

    __tablename__ = "style_tags"

    id = Column(Integer, primary_key=True, index=True)
    
    # Tag Info
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Hierarchy
    category = Column(String(100), index=True)  # e.g., "lighting", "mood", "location"
    parent_tag_id = Column(Integer)
    
    # Examples
    example_keywords = Column(Text)  # Comma-separated keywords
    
    # Usage Stats
    usage_count = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<StyleTag(id={self.id}, name={self.name})>"
