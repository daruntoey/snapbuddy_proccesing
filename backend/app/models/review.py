"""Review database model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    """Review model."""

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    photographer_id = Column(Integer, ForeignKey("photographers.id"), nullable=False, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    
    # Rating (1-5 stars)
    overall_rating = Column(Float, nullable=False)
    style_match_rating = Column(Float)  # How well photographer matched aesthetic
    professionalism_rating = Column(Float)
    communication_rating = Column(Float)
    value_rating = Column(Float)
    
    # Review Content
    title = Column(String(255))
    review_text = Column(Text)
    pros = Column(JSON)  # Array of positive aspects
    cons = Column(JSON)  # Array of areas for improvement
    
    # Media
    review_images = Column(JSON)  # URLs to example shots
    
    # Verification
    is_verified_booking = Column(Boolean, default=True)
    
    # Response
    photographer_response = Column(Text)
    photographer_response_date = Column(DateTime)
    
    # Engagement
    helpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    photographer = relationship("Photographer", back_populates="reviews")
    booking = relationship("Booking", back_populates="review")

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.overall_rating})>"
