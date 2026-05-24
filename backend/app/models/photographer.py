"""Photographer database model."""
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class Photographer(Base):
    """Photographer model."""

    __tablename__ = "photographers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile
    business_name = Column(String(255))
    bio = Column(Text)
    profile_image = Column(Text)
    cover_image = Column(Text)
    
    # Location
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    service_radius_km = Column(Integer, default=50)
    
    # Pricing
    hourly_rate = Column(Integer)
    package_rates = Column(JSON)  # Different package tiers
    
    # Availability
    is_accepting_bookings = Column(Boolean, default=True)
    available_days = Column(JSON)  # Array of available days
    blackout_dates = Column(JSON)  # Unavailable date ranges
    
    # Performance Metrics
    total_bookings = Column(Integer, default=0)
    completed_bookings = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    response_rate = Column(Float, default=1.0)
    response_time_hours = Column(Float)
    
    # Style & Expertise
    primary_styles = Column(JSON)  # Array of style tags
    expertise_tags = Column(JSON)  # Specialized areas
    equipment = Column(JSON)  # Camera/lens info
    
    # Verification
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    
    # Portfolio Embedding (average of all portfolio images)
    portfolio_embedding = Column(Vector(512))  # CLIP embedding dimension
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="photographer_profile")
    portfolios = relationship("Portfolio", back_populates="photographer", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="photographer")
    reviews = relationship("Review", back_populates="photographer")
    matching_results = relationship("MatchingResult", back_populates="photographer")

    def __repr__(self):
        return f"<Photographer(id={self.id}, business_name={self.business_name})>"
