from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import (
    ConflictException,
    UnauthorizedException,
    RateLimitException,
    BadRequestException
)
from app.core.rate_limiter import auth_rate_limiter
from app.models.user import User, StudentProfile
from app.repositories.user import user_repository, UserRepository
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
    UserUpdateRequest,
    PasswordChangeRequest,
    CurrentUserResponse,
    StudentProfileBrief
)

class AuthService:
    """Service handling user registration, authentication, tokens, and credential management."""
    def __init__(self, repo: UserRepository = user_repository):
        self.repo = repo

    def register(self, db: Session, request: UserRegisterRequest) -> User:
        """
        Registers a new user and creates their default student profile.
        Enforces unique email check and hashes passwords using Argon2id.
        """
        normalized_email = request.email.strip().lower()

        if self.repo.email_exists(db, normalized_email):
            raise ConflictException(
                message=f"A user with email '{normalized_email}' is already registered."
            )

        hashed_password = get_password_hash(request.password)

        new_user = User(
            email=normalized_email,
            full_name=request.full_name.strip(),
            password_hash=hashed_password,
            role=request.role,
            campus_name=request.campus_name.strip(),
            is_active=True
        )

        initial_profile = None
        if request.role == "student":
            initial_profile = StudentProfile(
                degree=request.degree or "B.Tech",
                branch=request.branch or "Computer Science and Engineering",
                graduation_year=request.graduation_year or 2026,
                skills=[],
                target_roles=[],
                preferred_locations=[],
                prep_hours_week=15
            )

        created_user = self.repo.create_user_with_profile(
            db,
            user=new_user,
            profile=initial_profile
        )
        return created_user

    def authenticate(
        self,
        db: Session,
        login_data: UserLoginRequest,
        client_identifier: str = "unknown"
    ) -> TokenResponse:
        """
        Authenticates a user by email and password with brute-force rate limit protection.
        Issues a signed JWT access token containing role and campus claims.
        """
        normalized_email = login_data.email.strip().lower()
        rate_key = f"login:{client_identifier}:{normalized_email}"

        # 1. Check rate limit
        is_limited, retry_after = auth_rate_limiter.is_rate_limited(
            key=rate_key,
            max_attempts=settings.RATE_LIMIT_LOGIN_ATTEMPTS,
            window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS
        )
        if is_limited:
            raise RateLimitException(
                message=f"Too many failed login attempts. Temporarily locked for security. Please try again in {retry_after} seconds."
            )

        # 2. Lookup user and verify password
        user = self.repo.get_by_email(db, normalized_email)
        if not user or not verify_password(login_data.password, user.password_hash):
            auth_rate_limiter.record_failure(rate_key)
            # Consistent safe error to prevent email enumeration
            raise UnauthorizedException(
                message="Invalid email address or password."
            )

        # 3. Check active status
        if not user.is_active:
            raise UnauthorizedException(
                message="Account has been suspended or deactivated. Please contact campus administration."
            )

        # 4. Clear failure count upon successful authentication
        auth_rate_limiter.reset(rate_key)

        # 5. Issue token
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_claims = {
            "email": user.email,
            "role": user.role,
            "campus_name": user.campus_name
        }
        token = create_access_token(
            subject=user.id,
            claims=token_claims,
            expires_delta=expires_delta
        )

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )

    def get_current_user_profile(self, db: Session, user: User) -> CurrentUserResponse:
        """Builds profile response including user identity and student academic profile if present."""
        profile_brief = None
        if user.profile:
            profile_brief = StudentProfileBrief.model_validate(user.profile)

        return CurrentUserResponse(
            user=UserResponse.model_validate(user),
            profile=profile_brief
        )

    def update_profile(self, db: Session, user: User, update_data: UserUpdateRequest) -> User:
        """Updates user account details."""
        if update_data.full_name is not None:
            user.full_name = update_data.full_name.strip()
        if update_data.campus_name is not None:
            user.campus_name = update_data.campus_name.strip()

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def change_password(
        self,
        db: Session,
        user: User,
        data: PasswordChangeRequest
    ) -> bool:
        """Verifies current password and updates to new Argon2id hashed password."""
        if not verify_password(data.current_password, user.password_hash):
            raise UnauthorizedException(message="Current password is incorrect.")

        if data.current_password == data.new_password:
            raise BadRequestException(message="New password must be different from current password.")

        new_hash = get_password_hash(data.new_password)
        self.repo.update_password_hash(db, user=user, password_hash=new_hash)
        return True

auth_service = AuthService()

