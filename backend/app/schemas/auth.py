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
