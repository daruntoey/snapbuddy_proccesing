"""Mood specification database model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, JSON, Float
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class MoodSpec(Base):
    """Mood specification model - unified aesthetic spec from user input."""

    __tablename__ = "mood_specs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # User Input
    text_description = Column(Text)  # User's natural language description
    reference_images = Column(JSON)  # URLs to uploaded reference images
    
    # AI-Extracted Features
    mood_tags = Column(JSON)  # Array of mood tags
    style_tags = Column(JSON)  # Array of style tags
    lighting_preferences = Column(JSON)
    location_styles = Column(JSON)
    pose_styles = Column(JSON)
    color_preferences = Column(JSON)
    
    # Embeddings
    text_embedding = Column(Vector(384))  # Sentence transformer embedding
    image_embeddings = Column(JSON)  # Array of CLIP embeddings from ref images
    combined_embedding = Column(Vector(512))  # Merged aesthetic embedding
    
    # Constraints
    budget_min = Column(Integer)
    budget_max = Column(Integer)
    preferred_location = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    max_distance_km = Column(Integer)
    preferred_dates = Column(JSON)
    
    # AI Analysis
    aesthetic_analysis = Column(JSON)  # Detailed breakdown from Gemini
    detected_intent = Column(Text)  # What user is really looking for
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="mood_specs")
    matching_results = relationship("MatchingResult", back_populates="mood_spec")
    bookings = relationship("Booking", back_populates="mood_spec")

    def __repr__(self):
        return f"<MoodSpec(id={self.id}, user_id={self.user_id})>"
