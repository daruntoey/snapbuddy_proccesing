"""Booking service."""
from app.schemas.booking import BookingCreate, BookingResponse
from app.models.booking import Booking, BookingStatus

class BookingService:
    async def create_booking(self, booking_data: BookingCreate, user_id: int, db):
        """Create new booking."""
        booking = Booking(
            user_id=user_id,
            photographer_id=booking_data.photographer_id,
            booking_date=booking_data.booking_date,
            booking_duration_hours=booking_data.booking_duration_hours,
            location=booking_data.location,
            quoted_price=1000,  # Calculate based on photographer rates
            status=BookingStatus.PENDING,
        )
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        
        return BookingResponse(
            id=booking.id,
            photographer_id=booking.photographer_id,
            booking_date=booking.booking_date,
            status=booking.status.value,
            quoted_price=booking.quoted_price,
        )

    async def get_user_bookings(self, user_id: int, db):
        """Get user bookings."""
        return {"bookings": []}

    async def get_booking(self, booking_id: int, user_id: int, db):
        """Get booking details."""
        return {}

booking_service = BookingService()
