"""Booking routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import booking_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create new booking."""
    return await booking_service.create_booking(booking_data, current_user.id, db)

@router.get("/")
async def list_bookings(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's bookings."""
    return await booking_service.get_user_bookings(current_user.id, db)

@router.get("/{booking_id}")
async def get_booking(
    booking_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get booking details."""
    return await booking_service.get_booking(booking_id, current_user.id, db)
