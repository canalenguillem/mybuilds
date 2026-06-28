"""Authentication routes."""
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database.models.users import User
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.auth import (
    AccessTokenResponse,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.models.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    user = AuthService(db).register(data)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        company=user.company,
        is_active=user.is_active,
        roles=user.role_names,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return AuthService(db).login(data, ip, user_agent)


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)) -> AccessTokenResponse:
    return AuthService(db).refresh(data.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(data: LogoutRequest, db: Session = Depends(get_db)) -> MessageResponse:
    AuthService(db).logout(data.refresh_token)
    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        company=user.company,
        is_active=user.is_active,
        roles=user.role_names,
        created_at=user.created_at,
    )
