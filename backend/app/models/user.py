"""User database model."""
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(50))
    profile_image = Column(Text)
    
    # Preferences
    preferred_location = Column(String(255))
    budget_range_min = Column(Integer)
    budget_range_max = Column(Integer)
    preferred_styles = Column(Text)  # JSON array
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_photographer = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    bookings = relationship("Booking", back_populates="user", foreign_keys="Booking.user_id")
    reviews = relationship("Review", back_populates="user")
    mood_specs = relationship("MoodSpec", back_populates="user")
    matching_results = relationship("MatchingResult", back_populates="user")
    photographer_profile = relationship(
        "Photographer",
        back_populates="user",
        uselist=False,
        foreign_keys="Photographer.user_id"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
