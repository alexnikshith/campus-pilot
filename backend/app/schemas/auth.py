from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.security import validate_password_strength

class UserRegisterRequest(BaseModel):
    """Payload for registering a new student or campus member."""
    email: EmailStr = Field(description="Student or official campus email address")
    full_name: str = Field(min_length=2, max_length=150, description="Legal full name")
    password: str = Field(min_length=8, description="Strong password meeting complexity requirements")
    campus_name: str = Field(default="National Institute of Engineering (NIE)", min_length=2, max_length=120)
    role: str = Field(default="student", description="Account role: student, campus_staff")
    
    # Optional academic details for automatic profile initialization
    degree: Optional[str] = Field(default="B.Tech", description="Academic degree (e.g. B.Tech, M.Tech)")
    branch: Optional[str] = Field(default="Computer Science and Engineering", description="Engineering branch")
    graduation_year: Optional[int] = Field(default=2026, ge=2020, le=2035, description="Expected graduation year")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        valid, error_msg = validate_password_strength(v)
        if not valid:
            raise ValueError(error_msg)
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = ["student", "campus_staff"]
        v_clean = v.strip().lower()
        if v_clean == "admin":
            raise ValueError("Administrative roles cannot be self-assigned during registration.")
        if v_clean not in allowed:
            raise ValueError(f"Invalid role. Permitted self-registration roles: {', '.join(allowed)}")
        return v_clean


class UserLoginRequest(BaseModel):
    """Payload for authenticating existing users."""
    email: EmailStr = Field(description="Registered email address")
    password: str = Field(description="Account password")


class UserResponse(BaseModel):
    """Public user identity representation (never leaks password_hash)."""
    id: int
    email: str
    full_name: str
    role: str
    campus_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class StudentProfileBrief(BaseModel):
    """Summary of student academic preferences."""
    id: Optional[int] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[Decimal] = None
    skills: List[str] = Field(default_factory=list)
    target_roles: List[str] = Field(default_factory=list)
    hostel_block: Optional[str] = None
    room_number: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class CurrentUserResponse(BaseModel):
    """Complete profile response for the authenticated user."""
    user: UserResponse
    profile: Optional[StudentProfileBrief] = None


class TokenResponse(BaseModel):
    """Bearer token response format with expiration and user payload."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token validity in seconds")
    user: UserResponse


class UserUpdateRequest(BaseModel):
    """Payload for updating user profile fields."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    campus_name: Optional[str] = Field(None, min_length=2, max_length=120)


class PasswordChangeRequest(BaseModel):
    """Payload for safely changing user password."""
    current_password: str = Field(description="Existing account password")
    new_password: str = Field(min_length=8, description="New password meeting complexity rules")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        valid, error_msg = validate_password_strength(v)
        if not valid:
            raise ValueError(error_msg)
        return v

