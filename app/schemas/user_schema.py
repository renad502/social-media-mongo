from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.enums.user_enums import UserRole
# Schema for user registration
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.USER
# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

# Schema for displaying user info
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    bio: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  

# Schema for updating user profile
class UserUpdate(BaseModel):
    bio: Optional[str]
    avatar_url: Optional[str]

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str
