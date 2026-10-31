from typing import List, Callable, Optional
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from app.repositories.user import user_repository

# Standard HTTP Bearer scheme without automatic error generation so we return our custom ErrorEnvelope
bearer_scheme = HTTPBearer(auto_error=False)

def get_client_ip(request: Request) -> str:
    """Extracts client IP or forwarder IP for rate limiting and logging."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

def get_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts, verifies, and decodes the JWT Bearer token,
    and returns the authenticated User entity from the database.
    """
    if not auth_header or not auth_header.credentials:
        raise UnauthorizedException(
            message="Authentication credentials required. Please provide a valid Bearer token in the Authorization header."
        )

    payload = decode_access_token(auth_header.credentials)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(message="Invalid token claims: user identifier missing.")

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise UnauthorizedException(message="Malformed user identifier in token claims.")

    user = user_repository.get(db, user_id)
    if not user:
        raise UnauthorizedException(message="User associated with this token no longer exists.")

    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensures that the authenticated user account is in an active state."""
    if not current_user.is_active:
        raise ForbiddenException(message="Account has been suspended or deactivated.")
    return current_user

def require_role(allowed_roles: List[str]) -> Callable[[User], User]:
    """
    Factory dependency enforcing Role-Based Access Control (RBAC).
    Restricts endpoint execution to users possessing one of the permitted roles.
    """
    def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                message=f"Access forbidden. This action requires one of the following roles: {', '.join(allowed_roles)}."
            )
        return current_user

    return role_checker

def verify_resource_ownership(current_user: User, resource_user_id: int) -> bool:
    """
    Enforces privacy boundaries preventing students from accessing or mutating other students' private data.
    Administrators are granted administrative oversight.
    """
    if current_user.role == "admin":
        return True
    if current_user.id != resource_user_id:
        raise ForbiddenException(
            message="Access denied. You do not have permission to view or modify another student's private data."
        )
    return True

