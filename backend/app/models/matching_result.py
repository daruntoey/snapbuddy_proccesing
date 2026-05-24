"""Matching result database model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text, JSON, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class MatchingResult(Base):
    """AI matching result model."""

    __tablename__ = "matching_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    photographer_id = Column(Integer, ForeignKey("photographers.id"), nullable=False, index=True)
    mood_spec_id = Column(Integer, ForeignKey("mood_specs.id"), nullable=False, index=True)
    
    # Overall Matching
    match_score = Column(Float, nullable=False, index=True)  # 0-100
    rank_position = Column(Integer)  # Position in recommendation list
    
    # Component Scores (weighted)
    style_similarity_score = Column(Float, nullable=False)  # 40% weight
    performance_score = Column(Float, nullable=False)  # 25% weight
    budget_fit_score = Column(Float, nullable=False)  # 15% weight
    availability_score = Column(Float, nullable=False)  # 10% weight
    distance_score = Column(Float, nullable=False)  # 10% weight
    
    # Raw Metrics
    vector_similarity = Column(Float)  # Cosine similarity from Qdrant
    distance_km = Column(Float)
    price_difference = Column(Integer)
    
    # AI Explanation
    explanation_text = Column(Text)  # Gemini-generated explanation
    explanation_highlights = Column(JSON)  # Key points
    matching_portfolio_ids = Column(JSON)  # IDs of most similar portfolio images
    
    # Prediction
    satisfaction_probability = Column(Float)  # ML-predicted success rate
    booking_probability = Column(Float)  # Likelihood of booking
    
    # User Interaction
    was_viewed = Column(Boolean, default=False)
    was_contacted = Column(Boolean, default=False)
    was_booked = Column(Boolean, default=False)
    user_feedback_score = Column(Integer)  # User rating of recommendation
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    viewed_at = Column(DateTime)
    contacted_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="matching_results")
    photographer = relationship("Photographer", back_populates="matching_results")
    mood_spec = relationship("MoodSpec", back_populates="matching_results")
    bookings = relationship("Booking", back_populates="matching_result")

    def __repr__(self):
        return f"<MatchingResult(id={self.id}, score={self.match_score})>"
