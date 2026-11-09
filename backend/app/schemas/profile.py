from decimal import Decimal
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from app.schemas.auth import UserResponse


class TaxonomyItem(BaseModel):
    category: str
    items: List[str]


class TaxonomyResponse(BaseModel):
    degrees: List[str]
    branches: List[str]
    skills_by_category: List[TaxonomyItem]
    target_roles: List[str]
    hostel_blocks: List[str]
    preferred_locations: List[str]


class ProfileCompletenessBreakdown(BaseModel):
    total_percentage: int = Field(ge=0, le=100)
    basic_info: int = Field(ge=0, le=20, description="Name, email, phone, campus (max 20)")
    academic_info: int = Field(ge=0, le=25, description="Degree, branch, graduation year, CGPA (max 25)")
    target_roles: int = Field(ge=0, le=20, description="Selected placement target roles (max 20)")
    skills: int = Field(ge=0, le=20, description="Technical skills inventory (max 20)")
    hostel_info: int = Field(ge=0, le=15, description="Hostel block & room number (max 15)")
    missing_fields: List[str] = Field(default_factory=list)
    next_step_recommendation: str


class StudentProfileBase(BaseModel):
    degree: str = Field(min_length=2, max_length=100, description="Degree name (e.g. B.Tech, M.Tech)")
    branch: str = Field(min_length=2, max_length=100, description="Engineering branch")
    graduation_year: int = Field(ge=2020, le=2035, description="Expected graduation year")
    cgpa: Optional[Decimal] = Field(None, ge=0.00, le=10.00, description="Cumulative Grade Point Average (0.00 to 10.00)")
    skills: List[str] = Field(default_factory=list, description="Technical and placement skills")
    target_roles: List[str] = Field(default_factory=list, description="Desired job roles")
    preferred_locations: Optional[List[str]] = Field(default_factory=list, description="Preferred employment locations")
    prep_hours_week: int = Field(default=15, ge=1, le=100, description="Weekly hours dedicated to placement prep")
    hostel_block: Optional[str] = Field(None, max_length=100, description="Hostel block or building name")
    room_number: Optional[str] = Field(None, max_length=50, description="Hostel room number")

    @field_validator("skills", "target_roles", "preferred_locations", mode="before")
    @classmethod
    def clean_string_list(cls, v: Any) -> List[str]:
        if not v:
            return []
        if isinstance(v, list):
            cleaned = []
            for item in v:
                if isinstance(item, str):
                    s = item.strip()
                    if s and s not in cleaned:
                        cleaned.append(s)
            return cleaned
        return []


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(BaseModel):
    degree: Optional[str] = Field(None, min_length=2, max_length=100)
    branch: Optional[str] = Field(None, min_length=2, max_length=100)
    graduation_year: Optional[int] = Field(None, ge=2020, le=2035)
    cgpa: Optional[Decimal] = Field(None, ge=0.00, le=10.00)
    skills: Optional[List[str]] = None
    target_roles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    prep_hours_week: Optional[int] = Field(None, ge=1, le=100)
    hostel_block: Optional[str] = Field(None, max_length=100)
    room_number: Optional[str] = Field(None, max_length=50)

    # Allow partial updates to phone_number and bio on the connected User
    phone_number: Optional[str] = Field(None, max_length=25)
    bio: Optional[str] = Field(None, max_length=1000)

    @field_validator("skills", "target_roles", "preferred_locations", mode="before")
    @classmethod
    def clean_string_list(cls, v: Any) -> Optional[List[str]]:
        if v is None:
            return None
        if isinstance(v, list):
            cleaned = []
            for item in v:
                if isinstance(item, str):
                    s = item.strip()
                    if s and s not in cleaned:
                        cleaned.append(s)
            return cleaned
        return []


class OnboardingRequest(BaseModel):
    """Payload submitted when a student completes the onboarding wizard."""
    degree: str = Field(min_length=2, max_length=100)
    branch: str = Field(min_length=2, max_length=100)
    graduation_year: int = Field(ge=2020, le=2035)
    cgpa: Optional[Decimal] = Field(None, ge=0.00, le=10.00)
    skills: List[str] = Field(min_length=1, description="At least one technical skill required")
    target_roles: List[str] = Field(min_length=1, description="At least one target job role required")
    preferred_locations: Optional[List[str]] = Field(default_factory=list)
    prep_hours_week: int = Field(default=15, ge=1, le=100)
    hostel_block: Optional[str] = None
    room_number: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None


class StudentProfileResponse(BaseModel):
    """Comprehensive academic profile response including user and completeness data."""
    id: int
    user_id: int
    user: UserResponse
    degree: str
    branch: str
    graduation_year: int
    cgpa: Optional[Decimal] = None
    skills: List[str]
    target_roles: List[str]
    preferred_locations: List[str]
    prep_hours_week: int
    hostel_block: Optional[str] = None
    room_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completeness: ProfileCompletenessBreakdown

    model_config = {
        "from_attributes": True
    }

