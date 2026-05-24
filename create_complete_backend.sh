#!/bin/bash

# Create API route files
mkdir -p backend/app/api/routes

# Auth routes
cat > backend/app/api/routes/__init__.py << 'EOF'
"""API routes."""
EOF

cat > backend/app/api/routes/auth.py << 'EOF'
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
EOF

# Upload routes
cat > backend/app/api/routes/upload.py << 'EOF'
"""File upload routes."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.upload_service import upload_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/reference-images")
async def upload_reference_images(
    files: List[UploadFile] = File(...),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload reference images for aesthetic analysis."""
    if len(files) > 5:
        raise HTTPException(400, "Maximum 5 images allowed")
    
    results = await upload_service.upload_reference_images(files, current_user.id, db)
    return {"images": results}
EOF

# Analysis routes
cat > backend/app/api/routes/analysis.py << 'EOF'
"""AI analysis routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.analysis import MoodAnalysisRequest, MoodAnalysisResponse
from app.services.analysis_service import analysis_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/mood", response_model=MoodAnalysisResponse)
async def analyze_mood(
    request: MoodAnalysisRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze mood from text and images."""
    return await analysis_service.analyze_user_mood(request, current_user.id, db)

@router.post("/extract-embedding")
async def extract_embedding(
    image_urls: List[str],
    current_user = Depends(get_current_user),
):
    """Extract embeddings from images."""
    return await analysis_service.extract_embeddings(image_urls)
EOF

# Matching routes
cat > backend/app/api/routes/matching.py << 'EOF'
"""Photographer matching routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.matching import MatchRequest, MatchResponse
from app.services.matching_service import matching_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/match-photographers", response_model=MatchResponse)
async def match_photographers(
    request: MatchRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Find and rank matching photographers."""
    return await matching_service.find_matches(request, current_user.id, db)

@router.get("/recommendations/{mood_spec_id}")
async def get_recommendations(
    mood_spec_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get saved recommendations."""
    return await matching_service.get_saved_recommendations(mood_spec_id, current_user.id, db)
EOF

# Photographers routes
cat > backend/app/api/routes/photographers.py << 'EOF'
"""Photographer routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas.photographer import PhotographerResponse

router = APIRouter()

@router.get("/{photographer_id}", response_model=PhotographerResponse)
async def get_photographer(
    photographer_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get photographer profile."""
    from app.repositories.photographer_repository import photographer_repo
    photographer = await photographer_repo.get_by_id(db, photographer_id)
    if not photographer:
        raise HTTPException(404, "Photographer not found")
    return photographer

@router.get("/")
async def list_photographers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    style: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List photographers with optional filtering."""
    from app.repositories.photographer_repository import photographer_repo
    photographers = await photographer_repo.list_photographers(db, skip, limit, style)
    return {"photographers": photographers, "total": len(photographers)}
EOF

# Bookings routes
cat > backend/app/api/routes/bookings.py << 'EOF'
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
EOF

# Users routes
cat > backend/app/api/routes/users.py << 'EOF'
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
EOF

# Create schemas
mkdir -p backend/app/schemas

cat > backend/app/schemas/__init__.py << 'EOF'
"""Pydantic schemas."""
EOF

cat > backend/app/schemas/auth.py << 'EOF'
"""Auth schemas."""
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
EOF

cat > backend/app/schemas/user.py << 'EOF'
"""User schemas."""
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    is_photographer: bool
    created_at: datetime

    class Config:
        from_attributes = True
EOF

cat > backend/app/schemas/analysis.py << 'EOF'
"""Analysis schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class MoodAnalysisRequest(BaseModel):
    text_description: str | None = None
    image_urls: List[str] = []
    budget_min: int | None = None
    budget_max: int | None = None
    location: str | None = None

class MoodAnalysisResponse(BaseModel):
    mood_spec_id: int
    mood_tags: List[str]
    style_tags: List[str]
    detected_intent: str
    aesthetic_summary: str
EOF

cat > backend/app/schemas/matching.py << 'EOF'
"""Matching schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class MatchRequest(BaseModel):
    mood_spec_id: int
    limit: int = 10

class PhotographerMatch(BaseModel):
    photographer_id: int
    business_name: str
    match_score: float
    style_similarity_score: float
    explanation: str
    profile_image: str | None
    hourly_rate: int
    average_rating: float
    location: str

class MatchResponse(BaseModel):
    matches: List[PhotographerMatch]
    total: int
EOF

cat > backend/app/schemas/photographer.py << 'EOF'
"""Photographer schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any

class PhotographerResponse(BaseModel):
    id: int
    business_name: str
    bio: str | None
    location: str
    hourly_rate: int
    average_rating: float
    total_reviews: int
    primary_styles: List[str]
    profile_image: str | None

    class Config:
        from_attributes = True
EOF

cat > backend/app/schemas/booking.py << 'EOF'
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
EOF

# Create services
mkdir -p backend/app/services

cat > backend/app/services/__init__.py << 'EOF'
"""Business logic services."""
EOF

cat > backend/app/services/auth_service.py << 'EOF'
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
EOF

cat > backend/app/services/upload_service.py << 'EOF'
"""File upload service."""
from typing import List
from fastapi import UploadFile
from google.cloud import storage
import uuid

from app.config import settings

class UploadService:
    def __init__(self):
        # Initialize GCS client
        self.bucket_name = settings.GCS_BUCKET_NAME

    async def upload_reference_images(self, files: List[UploadFile], user_id: int, db):
        """Upload images to GCS."""
        uploaded_urls = []
        
        for file in files:
            # Generate unique filename
            file_ext = file.filename.split('.')[-1]
            unique_filename = f"users/{user_id}/references/{uuid.uuid4()}.{file_ext}"
            
            # For now, return mock URLs
            # In production, upload to GCS
            mock_url = f"https://storage.googleapis.com/{self.bucket_name}/{unique_filename}"
            uploaded_urls.append(mock_url)
        
        return uploaded_urls

upload_service = UploadService()
EOF

cat > backend/app/services/analysis_service.py << 'EOF'
"""AI analysis service."""
from typing import List
from app.schemas.analysis import MoodAnalysisRequest, MoodAnalysisResponse
from app.ai.gemini_service import gemini_service
from app.ai.nlp_service import nlp_service
from app.ai.cv_service import cv_service
from app.ai.aesthetic_engine import aesthetic_engine
from app.models.mood_spec import MoodSpec

class AnalysisService:
    async def analyze_user_mood(self, request: MoodAnalysisRequest, user_id: int, db):
        """Analyze user's aesthetic preferences."""
        
        # Extract text features
        mood_analysis = {}
        if request.text_description:
            mood_analysis = await gemini_service.analyze_mood_from_text(request.text_description)
            text_embedding = await nlp_service.extract_text_embedding(request.text_description)
        else:
            text_embedding = None
        
        # Extract image features
        image_embeddings = []
        # For now, skip actual image processing
        
        # Create combined embedding
        if image_embeddings or text_embedding is not None:
            combined_embedding = await aesthetic_engine.merge_embeddings(
                image_embeddings, text_embedding
            )
        else:
            combined_embedding = None
        
        # Generate summary
        aesthetic_summary = await gemini_service.generate_aesthetic_summary({
            "mood_tags": mood_analysis.get("mood_tags", []),
            "style_tags": mood_analysis.get("style_tags", []),
            "text_description": request.text_description,
            "budget_min": request.budget_min,
            "budget_max": request.budget_max,
        })
        
        # Save mood spec
        mood_spec = MoodSpec(
            user_id=user_id,
            text_description=request.text_description,
            mood_tags=mood_analysis.get("mood_tags", []),
            style_tags=mood_analysis.get("style_tags", []),
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            preferred_location=request.location,
        )
        db.add(mood_spec)
        await db.commit()
        await db.refresh(mood_spec)
        
        return MoodAnalysisResponse(
            mood_spec_id=mood_spec.id,
            mood_tags=mood_analysis.get("mood_tags", []),
            style_tags=mood_analysis.get("style_tags", []),
            detected_intent=mood_analysis.get("detected_intent", ""),
            aesthetic_summary=aesthetic_summary,
        )

    async def extract_embeddings(self, image_urls: List[str]):
        """Extract embeddings from images."""
        # Implement image embedding extraction
        return {"embeddings": []}

analysis_service = AnalysisService()
EOF

cat > backend/app/services/matching_service.py << 'EOF'
"""Photographer matching service."""
from app.schemas.matching import MatchRequest, MatchResponse, PhotographerMatch
from app.ai.matching_engine import matching_engine
from app.ai.ranking_engine import ranking_engine
from app.ai.explanation_engine import explanation_engine

class MatchingService:
    async def find_matches(self, request: MatchRequest, user_id: int, db):
        """Find matching photographers."""
        # For now, return mock matches
        return MatchResponse(
            matches=[
                PhotographerMatch(
                    photographer_id=1,
                    business_name="Studio One",
                    match_score=95.5,
                    style_similarity_score=98.0,
                    explanation="Perfect match for Korean cafe aesthetic with warm lighting expertise.",
                    profile_image=None,
                    hourly_rate=150,
                    average_rating=4.8,
                    location="Seoul, South Korea",
                )
            ],
            total=1,
        )

    async def get_saved_recommendations(self, mood_spec_id: int, user_id: int, db):
        """Get saved recommendations."""
        return {"recommendations": []}

matching_service = MatchingService()
EOF

cat > backend/app/services/booking_service.py << 'EOF'
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
EOF

# Create repositories
mkdir -p backend/app/repositories

cat > backend/app/repositories/__init__.py << 'EOF'
"""Data access layer."""
EOF

cat > backend/app/repositories/photographer_repository.py << 'EOF'
"""Photographer repository."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.photographer import Photographer

class PhotographerRepository:
    async def get_by_id(self, db: AsyncSession, photographer_id: int) -> Optional[Photographer]:
        result = await db.execute(select(Photographer).where(Photographer.id == photographer_id))
        return result.scalar_one_or_none()

    async def list_photographers(
        self, db: AsyncSession, skip: int = 0, limit: int = 20, style: Optional[str] = None
    ) -> List[Photographer]:
        query = select(Photographer).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

photographer_repo = PhotographerRepository()
EOF

# Create utils
mkdir -p backend/app/utils

cat > backend/app/utils/__init__.py << 'EOF'
"""Utility functions."""
EOF

# Create __init__ files
touch backend/app/__init__.py

echo "Complete backend structure created!"

