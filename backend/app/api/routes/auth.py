"""Authentication routes."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import Token, UserCreate, UserLogin
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register new user."""
    return await auth_service.register_user(user_data, db)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Login user."""
    return await auth_service.authenticate_user(form_data.username, form_data.password, db)

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    return await auth_service.refresh_access_token(refresh_token)
