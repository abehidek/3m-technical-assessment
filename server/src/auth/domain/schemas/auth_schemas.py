from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base schema for User"""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""

    password: str


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class Token(BaseModel):
    """Schema for JWT token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data"""

    email: str | None = None
