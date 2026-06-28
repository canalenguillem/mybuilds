"""Authentication request/response schemas (match API_SPECIFICATIONS.md)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = None
    company: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class UserPublic(BaseModel):
    """User shape embedded in the login response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    roles: list[str] = []
    permissions: list[str] = []


class UserResponse(BaseModel):
    """Returned by /register and /auth/me."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    full_name: str | None = None
    company: str | None = None
    is_active: bool = True
    roles: list[str] = []
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
