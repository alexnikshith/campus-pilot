from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import StudentProfile
from app.repositories.base import BaseRepository
from app.schemas.profile import StudentProfileCreate, StudentProfileUpdate


class StudentProfileRepository(BaseRepository[StudentProfile, StudentProfileCreate, StudentProfileUpdate]):
    """Specialized repository for student academic profile management."""
    def __init__(self):
        super().__init__(StudentProfile)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[StudentProfile]:
        """Fetch the student profile associated with a specific user ID."""
        stmt = select(StudentProfile).where(StudentProfile.user_id == user_id)
        return db.scalar(stmt)

    def upsert_profile(
        self,
        db: Session,
        *,
        user_id: int,
        profile_in: StudentProfileUpdate
    ) -> StudentProfile:
        """
        Updates an existing student profile or creates a new one if not yet initialized.
        """
        profile = self.get_by_user_id(db, user_id=user_id)
        update_data = profile_in.model_dump(exclude_unset=True)

        # Remove User-specific fields that belong on User model, not StudentProfile
        update_data.pop("phone_number", None)
        update_data.pop("bio", None)

        if not profile:
            # Create a new profile with required fields defaulting if not supplied
            profile = StudentProfile(
                user_id=user_id,
                degree=update_data.get("degree", "B.Tech"),
                branch=update_data.get("branch", "Computer Science and Engineering"),
                graduation_year=update_data.get("graduation_year", 2026),
                cgpa=update_data.get("cgpa", None),
                skills=update_data.get("skills", []),
                target_roles=update_data.get("target_roles", []),
                preferred_locations=update_data.get("preferred_locations", []),
                prep_hours_week=update_data.get("prep_hours_week", 15),
                hostel_block=update_data.get("hostel_block", None),
                room_number=update_data.get("room_number", None),
            )
            db.add(profile)
        else:
            for field, value in update_data.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)
            db.add(profile)

        db.commit()
        db.refresh(profile)
        return profile


profile_repository = StudentProfileRepository()

