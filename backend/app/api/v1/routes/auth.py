from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import (
    get_client_ip,
    get_current_active_user,
    require_role,
    verify_resource_ownership
)
from app.models.user import User
from app.schemas.common import ResponseEnvelope
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
    UserUpdateRequest,
    PasswordChangeRequest,
    CurrentUserResponse
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication & Account"])

@router.post(
    "/register",
    response_model=ResponseEnvelope[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student or campus member"
)
def register(
    register_data: UserRegisterRequest,
    db: Session = Depends(get_db)
) -> ResponseEnvelope[UserResponse]:
    """
    Registers a new student or campus account:
    - Enforces Argon2id password hashing.
    - Validates email uniqueness.
    - Automatically initializes default student profile.
    - Restricts administrative self-registration.
    """
    created_user = auth_service.register(db, register_data)
    return ResponseEnvelope(
        success=True,
        data=UserResponse.model_validate(created_user),
        message="Account registered successfully. You may now log in."
    )


@router.post(
    "/login",
    response_model=ResponseEnvelope[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and obtain JWT access token"
)
def login(
    login_data: UserLoginRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> ResponseEnvelope[TokenResponse]:
    """
    Authenticates user with email and password:
    - Protects against brute-force attacks via rate limiting.
    - Verifies Argon2id password hash.
    - Issues a signed Bearer JWT token with campus and role claims.
    """
    client_ip = get_client_ip(request)
    token_response = auth_service.authenticate(db, login_data, client_identifier=client_ip)
    return ResponseEnvelope(
        success=True,
        data=token_response,
        message="Authentication successful."
    )


@router.post(
    "/logout",
    response_model=ResponseEnvelope[dict],
    status_code=status.HTTP_200_OK,
    summary="Invalidate session and log out"
)
def logout(
    current_user: User = Depends(get_current_active_user)
) -> ResponseEnvelope[dict]:
    """
    Logs out the authenticated user.
    Instructs the client to discard the access token.
    """
    return ResponseEnvelope(
        success=True,
        data={"user_id": current_user.id, "logged_out": True},
        message="Logged out successfully. Please discard the stored token."
    )


@router.get(
    "/me",
    response_model=ResponseEnvelope[CurrentUserResponse],
    status_code=status.HTTP_200_OK,
    summary="Fetch profile of currently authenticated user"
)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> ResponseEnvelope[CurrentUserResponse]:
    """
    Retrieves full account details and linked student academic profile.
    """
    profile_response = auth_service.get_current_user_profile(db, current_user)
    return ResponseEnvelope(
        success=True,
        data=profile_response,
        message="Profile retrieved successfully."
    )


@router.put(
    "/me",
    response_model=ResponseEnvelope[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Update basic account information"
)
def update_current_user_profile(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> ResponseEnvelope[UserResponse]:
    """
    Updates basic user identity details (full name, campus name).
    """
    updated_user = auth_service.update_profile(db, current_user, update_data)
    return ResponseEnvelope(
        success=True,
        data=UserResponse.model_validate(updated_user),
        message="Account details updated successfully."
    )


@router.post(
    "/change-password",
    response_model=ResponseEnvelope[dict],
    status_code=status.HTTP_200_OK,
    summary="Change account password"
)
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> ResponseEnvelope[dict]:
    """
    Safely changes account password after verifying current credentials.
    """
    auth_service.change_password(db, current_user, data)
    return ResponseEnvelope(
        success=True,
        data={"updated": True},
        message="Password changed successfully. Please use your new password on next login."
    )


@router.get(
    "/admin-check",
    response_model=ResponseEnvelope[dict],
    status_code=status.HTTP_200_OK,
    summary="Verify administrator privileges (Role-Based Authorization)"
)
def admin_only_check(
    admin_user: User = Depends(require_role(["admin"]))
) -> ResponseEnvelope[dict]:
    """
    Endpoint protected by administrative role guard.
    Returns 403 Forbidden to regular students or staff.
    """
    return ResponseEnvelope(
        success=True,
        data={"admin_id": admin_user.id, "email": admin_user.email, "role": admin_user.role},
        message="Administrative authorization confirmed."
    )


@router.get(
    "/student-private-data/{user_id}",
    response_model=ResponseEnvelope[dict],
    status_code=status.HTTP_200_OK,
    summary="Access private student record (Ownership check verification)"
)
def get_private_student_record(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
) -> ResponseEnvelope[dict]:
    """
    Demonstrates student isolation boundary:
    Students can only view their own private data; administrators can view any.
    """
    verify_resource_ownership(current_user, user_id)
    return ResponseEnvelope(
        success=True,
        data={"accessed_user_id": user_id, "access_granted_to": current_user.email},
        message="Private data access authorized."
    )

