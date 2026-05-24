"""Booking database model."""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class BookingStatus(str, Enum):
    """Booking status enum."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Booking(Base):
    """Booking model."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    photographer_id = Column(Integer, ForeignKey("photographers.id"), nullable=False, index=True)
    matching_result_id = Column(Integer, ForeignKey("matching_results.id"))
    
    # Booking Details
    booking_date = Column(DateTime, nullable=False)
    booking_duration_hours = Column(Integer, nullable=False)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Pricing
    quoted_price = Column(Integer, nullable=False)
    final_price = Column(Integer)
    deposit_amount = Column(Integer)
    
    # Status
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False, index=True)
    
    # Aesthetic Requirements
    mood_spec_id = Column(Integer, ForeignKey("mood_specs.id"))
    reference_images = Column(JSON)  # URLs to reference images
    style_preferences = Column(JSON)
    special_requests = Column(Text)
    
    # Communication
    messages = Column(JSON)  # Message thread
    photographer_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = Column(DateTime)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="bookings", foreign_keys=[user_id])
    photographer = relationship("Photographer", back_populates="bookings")
    mood_spec = relationship("MoodSpec", back_populates="bookings")
    matching_result = relationship("MatchingResult", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)

    def __repr__(self):
        return f"<Booking(id={self.id}, status={self.status})>"
