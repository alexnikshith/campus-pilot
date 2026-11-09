from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_active_user, verify_resource_ownership
from app.schemas.common import ResponseEnvelope
from app.schemas.profile import (
    TaxonomyResponse,
    ProfileCompletenessBreakdown,
    StudentProfileUpdate,
    OnboardingRequest,
    StudentProfileResponse,
)
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profile", tags=["Student Profile & Onboarding"])


@router.get(
    "/taxonomy",
    response_model=ResponseEnvelope[TaxonomyResponse],
    summary="Get standard taxonomy catalogs",
    description="Returns standard catalogs for degrees, branches, skills by category, target roles, hostel blocks, and locations."
)
def get_profile_taxonomy():
    taxonomy = profile_service.get_taxonomy()
    return ResponseEnvelope(
        success=True,
        data=taxonomy,
        message="Profile taxonomy catalog retrieved successfully"
    )


@router.get(
    "",
    response_model=ResponseEnvelope[StudentProfileResponse],
    summary="Get current user academic profile",
    description="Retrieves the authenticated student's full profile including 5-dimension completeness score."
)
def get_current_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = profile_service.get_profile_by_user(db, current_user)
    return ResponseEnvelope(
        success=True,
        data=profile,
        message="Student academic profile retrieved successfully"
    )


@router.put(
    "",
    response_model=ResponseEnvelope[StudentProfileResponse],
    summary="Update current student profile",
    description="Updates academic details (degree, branch, graduation year, CGPA, skills, target roles, hostel details)."
)
def update_current_profile(
    profile_in: StudentProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated = profile_service.update_profile(db, current_user, profile_in)
    return ResponseEnvelope(
        success=True,
        data=updated,
        message="Student profile updated successfully"
    )


@router.get(
    "/completeness",
    response_model=ResponseEnvelope[ProfileCompletenessBreakdown],
    summary="Get profile completeness breakdown",
    description="Returns the weighted 0-100% completeness breakdown across Basic, Academic, Roles, Skills, and Hostel dimensions."
)
def get_profile_completeness(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = profile_service.get_profile_by_user(db, current_user)
    return ResponseEnvelope(
        success=True,
        data=profile.completeness,
        message="Profile completeness breakdown calculated successfully"
    )


@router.post(
    "/onboarding",
    response_model=ResponseEnvelope[StudentProfileResponse],
    status_code=status.HTTP_200_OK,
    summary="Complete multi-step onboarding wizard",
    description="Processes the full onboarding submission (academics, target roles, skills, and living details) in a single atomic transaction."
)
def complete_student_onboarding(
    onboarding_in: OnboardingRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    result = profile_service.complete_onboarding(db, current_user, onboarding_in)
    return ResponseEnvelope(
        success=True,
        data=result,
        message="Student onboarding completed successfully"
    )


@router.get(
    "/{user_id}",
    response_model=ResponseEnvelope[StudentProfileResponse],
    summary="Get student profile by user ID",
    description="Retrieves a specific student's profile. Restricted to the student themselves, campus staff, or administrators."
)
def get_profile_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    verify_resource_ownership(current_user, user_id)
    profile = profile_service.get_profile_by_user_id(db, user_id)
    return ResponseEnvelope(
        success=True,
        data=profile,
        message="Student academic profile retrieved successfully"
    )

