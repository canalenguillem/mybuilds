"""Authentication business logic: register, login, refresh, logout."""
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.users import ROLE_VIEWER, Role, User, UserSession
from app.exceptions import ConflictError, UnauthorizedError
from app.models.auth import (
    AccessTokenResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserPublic,
)
from app.utils.security import (
    REFRESH_TOKEN,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    # ── Registration ────────────────────────────────────────────
    def register(self, data: RegisterRequest) -> User:
        existing = self.db.scalar(
            select(User).where(
                (User.email == data.email) | (User.username == data.username)
            )
        )
        if existing:
            field = "email" if existing.email == data.email else "username"
            raise ConflictError(f"A user with this {field} already exists.", {"field": field})

        user = User(
            email=data.email,
            username=data.username,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            company=data.company,
        )
        # New users get the Viewer role by default.
        viewer = self.db.scalar(select(Role).where(Role.name == ROLE_VIEWER))
        if viewer:
            user.roles.append(viewer)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ── Login ───────────────────────────────────────────────────
    def login(self, data: LoginRequest, ip: str | None, user_agent: str | None) -> TokenResponse:
        user = self.db.scalar(select(User).where(User.email == data.email))
        if not user or not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedError("This account is inactive.")

        access = create_access_token(
            user.id, roles=user.role_names, permissions=user.permission_names
        )
        refresh = create_refresh_token(user.id)
        self._store_session(user.id, refresh, ip, user_agent)

        user.last_login = datetime.now(timezone.utc)
        self.db.commit()

        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.access_token_expire_minutes * 60,
            user=UserPublic(
                id=user.id,
                email=user.email,
                username=user.username,
                roles=user.role_names,
                permissions=user.permission_names,
            ),
        )

    # ── Refresh ─────────────────────────────────────────────────
    def refresh(self, refresh_token: str) -> AccessTokenResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError as exc:
            raise UnauthorizedError("Invalid or expired refresh token.") from exc

        if payload.get("type") != REFRESH_TOKEN:
            raise UnauthorizedError("Provided token is not a refresh token.")

        session = self.db.scalar(
            select(UserSession).where(UserSession.token_hash == hash_token(refresh_token))
        )
        if not session or session.revoked_at is not None:
            raise UnauthorizedError("Refresh token has been revoked.")

        user = self.db.get(User, int(payload["sub"]))
        if not user or not user.is_active:
            raise UnauthorizedError("User no longer exists or is inactive.")

        access = create_access_token(
            user.id, roles=user.role_names, permissions=user.permission_names
        )
        return AccessTokenResponse(
            access_token=access,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    # ── Logout ──────────────────────────────────────────────────
    def logout(self, refresh_token: str) -> None:
        session = self.db.scalar(
            select(UserSession).where(UserSession.token_hash == hash_token(refresh_token))
        )
        if session and session.revoked_at is None:
            session.revoked_at = datetime.now(timezone.utc)
            self.db.commit()

    # ── Helpers ─────────────────────────────────────────────────
    def _store_session(self, user_id: int, refresh_token: str, ip: str | None, ua: str | None) -> None:
        expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        self.db.add(
            UserSession(
                user_id=user_id,
                token_hash=hash_token(refresh_token),
                ip_address=ip,
                user_agent=ua,
                expires_at=expires,
            )
        )
