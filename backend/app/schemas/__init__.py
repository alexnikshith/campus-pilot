"""
PlacementPilot Pydantic Schemas Package
"""

from app.schemas.common import (
    ResponseEnvelope,
    ErrorDetail,
    ErrorEnvelope,
    PaginationParams,
    PaginatedResponse
)
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    StudentProfileBrief,
    CurrentUserResponse,
    TokenResponse,
    UserUpdateRequest,
    PasswordChangeRequest
)

__all__ = [
    "ResponseEnvelope",
    "ErrorDetail",
    "ErrorEnvelope",
    "PaginationParams",
    "PaginatedResponse",
    "UserRegisterRequest",
    "UserLoginRequest",
    "UserResponse",
    "StudentProfileBrief",
    "CurrentUserResponse",
    "TokenResponse",
    "UserUpdateRequest",
    "PasswordChangeRequest"
]
