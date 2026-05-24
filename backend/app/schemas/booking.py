"""Booking schemas."""
from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    photographer_id: int
    booking_date: datetime
    booking_duration_hours: int
    location: str
    mood_spec_id: int | None = None
    special_requests: str | None = None

class BookingResponse(BaseModel):
    id: int
    photographer_id: int
    booking_date: datetime
    status: str
    quoted_price: int

    class Config:
        from_attributes = True
