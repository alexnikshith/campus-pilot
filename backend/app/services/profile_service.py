from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User, StudentProfile
from app.repositories.profile import profile_repository
from app.repositories.user import user_repository
from app.schemas.auth import UserResponse
from app.schemas.profile import (
    TaxonomyItem,
    TaxonomyResponse,
    ProfileCompletenessBreakdown,
    StudentProfileUpdate,
    OnboardingRequest,
    StudentProfileResponse,
)
from app.core.exceptions import EntityNotFoundException, BadRequestException


class StudentProfileService:
    """Domain service managing student profiles, taxonomy catalogs, and completeness scoring."""

    @staticmethod
    def get_taxonomy() -> TaxonomyResponse:
        """Returns standard taxonomies for engineering degrees, branches, skills, and target roles."""
        return TaxonomyResponse(
            degrees=[
                "B.Tech",
                "B.E.",
                "M.Tech",
                "BCA",
                "MCA",
                "B.Sc Computer Science",
            ],
            branches=[
                "Computer Science and Engineering",
                "Information Technology",
                "Artificial Intelligence and Data Science",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
            ],
            skills_by_category=[
                TaxonomyItem(
                    category="Programming Languages",
                    items=["Python", "Java", "C++", "C", "JavaScript", "TypeScript", "Go", "SQL"],
                ),
                TaxonomyItem(
                    category="Web & Backend Frameworks",
                    items=["React", "Node.js", "FastAPI", "Django", "Spring Boot", "Express.js", "Next.js"],
                ),
                TaxonomyItem(
                    category="Databases & Caching",
                    items=["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite"],
                ),
                TaxonomyItem(
                    category="Cloud & DevOps",
                    items=["AWS", "Docker", "Kubernetes", "Git & GitHub", "Linux CLI", "CI/CD"],
                ),
                TaxonomyItem(
                    category="Core Computer Science",
                    items=[
                        "Data Structures & Algorithms",
                        "Database Management Systems (DBMS)",
                        "Operating Systems",
                        "Computer Networks",
                        "System Design",
                        "Object-Oriented Programming (OOP)",
                    ],
                ),
                TaxonomyItem(
                    category="Data Science & Machine Learning",
                    items=["Machine Learning", "Deep Learning", "Pandas & NumPy", "NLP", "TensorFlow/PyTorch"],
                ),
            ],
            target_roles=[
                "Software Development Engineer (SDE)",
                "Backend Developer",
                "Frontend Developer",
                "Full-Stack Developer",
                "Data Analyst / Data Engineer",
                "AI / ML Engineer",
                "Cloud & DevOps Engineer",
                "QA / Test Automation Engineer",
            ],
            hostel_blocks=[
                "Aryabhatta Block",
                "Bhaskara Block",
                "Visvesvaraya Block",
                "Ramanujan Block",
                "Kalam Block",
                "Gargi Hall (Girls)",
                "Maitreyi Hall (Girls)",
                "Day Scholar / Off-Campus",
            ],
            preferred_locations=[
                "Bangalore",
                "Hyderabad",
                "Pune",
                "Delhi NCR / Gurgaon",
                "Mumbai",
                "Chennai",
                "Remote",
            ],
        )

    def calculate_completeness(
        self,
        user: User,
        profile: Optional[StudentProfile]
    ) -> ProfileCompletenessBreakdown:
        """
        Calculates a deterministic 0-100% profile completeness score across 5 weighted dimensions.
        """
        missing: List[str] = []

        # 1. Basic Identity (Max 20)
        basic_score = 0
        if user.full_name and len(user.full_name.strip()) >= 2:
            basic_score += 10
        else:
            missing.append("Legal full name")

        if user.campus_name and len(user.campus_name.strip()) >= 2:
            basic_score += 5
        else:
            missing.append("Verified campus name")

        if user.email:
            basic_score += 5

        # 2. Academic Information (Max 25)
        academic_score = 0
        if profile and profile.degree:
            academic_score += 5
        else:
            missing.append("Academic degree")

        if profile and profile.branch:
            academic_score += 10
        else:
            missing.append("Engineering branch")

        if profile and profile.graduation_year:
            academic_score += 5
        else:
            missing.append("Expected graduation year")

        if profile and profile.cgpa is not None:
            academic_score += 5
        else:
            missing.append("Cumulative CGPA")

        # 3. Target Placement Roles (Max 20)
        roles_score = 0
        roles_count = len(profile.target_roles) if profile and profile.target_roles else 0
        if roles_count >= 2:
            roles_score = 20
        elif roles_count == 1:
            roles_score = 10
            missing.append("Add a 2nd target role for better matchmaking")
        else:
            missing.append("Target placement roles")

        # 4. Technical Skills Inventory (Max 20)
        skills_score = 0
        skills_count = len(profile.skills) if profile and profile.skills else 0
        if skills_count >= 5:
            skills_score = 20
        elif skills_count >= 2:
            skills_score = 10
            missing.append("Add at least 5 technical skills")
        else:
            missing.append("Technical skills inventory (min 5)")

        # 5. Hostel & Campus Residency (Max 15)
        hostel_score = 0
        if profile and profile.hostel_block:
            hostel_score += 10
        else:
            missing.append("Hostel block or day scholar status")

        if profile and profile.room_number:
            hostel_score += 5
        elif profile and profile.hostel_block and "Day Scholar" not in profile.hostel_block:
            missing.append("Hostel room number")

        total = basic_score + academic_score + roles_score + skills_score + hostel_score
        total = min(100, max(0, total))

        # Contextual recommendation
        if total == 100:
            recommendation = "Your student profile is 100% complete and fully verified for campus placements!"
        elif "Technical skills inventory (min 5)" in missing or "Add at least 5 technical skills" in missing:
            recommendation = "Add at least 5 technical skills to unlock accurate diagnostic study plan generation."
        elif "Target placement roles" in missing:
            recommendation = "Select your target engineering job roles to tailor upcoming assessment benchmarks."
        elif "Cumulative CGPA" in missing:
            recommendation = "Add your verified CGPA to filter opportunities matching campus placement eligibility."
        else:
            recommendation = f"Complete {missing[0]} to raise your placement readiness score."

        return ProfileCompletenessBreakdown(
            total_percentage=total,
            basic_info=basic_score,
            academic_info=academic_score,
            target_roles=roles_score,
            skills=skills_score,
            hostel_info=hostel_score,
            missing_fields=missing,
            next_step_recommendation=recommendation,
        )

    def get_profile_by_user(self, db: Session, user: User) -> StudentProfileResponse:
        """Fetch the current user's profile with completeness calculation."""
        profile = profile_repository.get_by_user_id(db, user_id=user.id)
        if not profile:
            # Auto-create empty profile if none exists
            profile = profile_repository.upsert_profile(
                db,
                user_id=user.id,
                profile_in=StudentProfileUpdate(
                    degree="B.Tech",
                    branch="Computer Science and Engineering",
                    graduation_year=2026,
                )
            )

        completeness = self.calculate_completeness(user, profile)

        return StudentProfileResponse(
            id=profile.id,
            user_id=user.id,
            user=UserResponse.model_validate(user),
            degree=profile.degree,
            branch=profile.branch,
            graduation_year=profile.graduation_year,
            cgpa=profile.cgpa,
            skills=profile.skills or [],
            target_roles=profile.target_roles or [],
            preferred_locations=profile.preferred_locations or [],
            prep_hours_week=profile.prep_hours_week,
            hostel_block=profile.hostel_block,
            room_number=profile.room_number,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            completeness=completeness,
        )

    def update_profile(
        self,
        db: Session,
        user: User,
        profile_in: StudentProfileUpdate
    ) -> StudentProfileResponse:
        """Update academic details and optional user-level contact info."""
        # Update user fields if provided
        user_modified = False
        if profile_in.phone_number is not None:
            user.phone_number = profile_in.phone_number.strip() or None
            user_modified = True
        if profile_in.bio is not None:
            user.bio = profile_in.bio.strip() or None
            user_modified = True

        if user_modified:
            db.add(user)
            db.commit()
            db.refresh(user)

        # Update profile
        profile = profile_repository.upsert_profile(db, user_id=user.id, profile_in=profile_in)
        completeness = self.calculate_completeness(user, profile)

        return StudentProfileResponse(
            id=profile.id,
            user_id=user.id,
            user=UserResponse.model_validate(user),
            degree=profile.degree,
            branch=profile.branch,
            graduation_year=profile.graduation_year,
            cgpa=profile.cgpa,
            skills=profile.skills or [],
            target_roles=profile.target_roles or [],
            preferred_locations=profile.preferred_locations or [],
            prep_hours_week=profile.prep_hours_week,
            hostel_block=profile.hostel_block,
            room_number=profile.room_number,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            completeness=completeness,
        )

    def complete_onboarding(
        self,
        db: Session,
        user: User,
        onboarding_in: OnboardingRequest
    ) -> StudentProfileResponse:
        """Processes submission from the multi-step onboarding wizard."""
        if not onboarding_in.skills:
            raise BadRequestException("Please select or enter at least one technical skill.")
        if not onboarding_in.target_roles:
            raise BadRequestException("Please select at least one target placement role.")

        profile_update = StudentProfileUpdate(
            degree=onboarding_in.degree,
            branch=onboarding_in.branch,
            graduation_year=onboarding_in.graduation_year,
            cgpa=onboarding_in.cgpa,
            skills=onboarding_in.skills,
            target_roles=onboarding_in.target_roles,
            preferred_locations=onboarding_in.preferred_locations or [],
            prep_hours_week=onboarding_in.prep_hours_week,
            hostel_block=onboarding_in.hostel_block,
            room_number=onboarding_in.room_number,
            phone_number=onboarding_in.phone_number,
            bio=onboarding_in.bio,
        )

        return self.update_profile(db, user, profile_update)

    def get_profile_by_user_id(
        self,
        db: Session,
        target_user_id: int
    ) -> StudentProfileResponse:
        """Admin or campus staff lookup of any student's academic profile."""
        target_user = user_repository.get(db, target_user_id)
        if not target_user:
            raise EntityNotFoundException(f"User with ID {target_user_id} does not exist.")

        return self.get_profile_by_user(db, target_user)


profile_service = StudentProfileService()

