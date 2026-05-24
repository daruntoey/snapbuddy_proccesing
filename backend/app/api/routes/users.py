"""User routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(get_current_user),
):
    """Get current user profile."""
    return current_user
