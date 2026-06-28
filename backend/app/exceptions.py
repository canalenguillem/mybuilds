"""Custom application exceptions mapped to the standard error envelope."""
from typing import Any


class AppException(Exception):
    """Base application exception carrying an HTTP status and error code."""

    status_code: int = 500
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class BadRequestError(AppException):
    status_code = 400
    code = "INVALID_INPUT"


class UnauthorizedError(AppException):
    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(AppException):
    status_code = 403
    code = "FORBIDDEN"


class NotFoundError(AppException):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(AppException):
    status_code = 409
    code = "CONFLICT"
