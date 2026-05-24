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
