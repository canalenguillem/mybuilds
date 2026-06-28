"""Shared FastAPI dependencies: DB session, current user, RBAC guards."""
from collections.abc import Callable

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models.users import User
from app.exceptions import ForbiddenError, UnauthorizedError
from app.utils.security import ACCESS_TOKEN, decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from a Bearer access token."""
    if credentials is None:
        raise UnauthorizedError("Authentication credentials were not provided.")

    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Invalid or expired access token.") from exc

    if payload.get("type") != ACCESS_TOKEN:
        raise UnauthorizedError("Provided token is not an access token.")

    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise UnauthorizedError("User no longer exists or is inactive.")

    request.state.user_id = user.id
    return user


def require_roles(*roles: str) -> Callable[[User], User]:
    """Dependency factory enforcing that the user has at least one of ``roles``."""

    def checker(user: User = Depends(get_current_user)) -> User:
        if not set(roles).intersection(user.role_names):
            raise ForbiddenError("You do not have permission to perform this action.")
        return user

    return checker
