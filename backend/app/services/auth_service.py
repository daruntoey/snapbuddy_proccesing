"""Authentication service."""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class AuthService:
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> Token:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(400, "Email already registered")
        
        # Create user
        hashed_password = self.get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Create tokens
        access_token = self.create_access_token(data={"sub": str(new_user.id)})
        return Token(access_token=access_token)

    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> Token:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(401, "Incorrect email or password")
        
        access_token = self.create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token)

    async def refresh_access_token(self, refresh_token: str) -> Token:
        # Implement refresh logic
        raise HTTPException(501, "Not implemented")

auth_service = AuthService()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
