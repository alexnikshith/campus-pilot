from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Boolean, Integer, Numeric, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.assessment import AssessmentAttempt
    from app.models.study_plan import StudyPlan
    from app.models.resume import Resume
    from app.models.mock_interview import MockInterview
    from app.models.opportunity import SavedOpportunity, ApplicationTracking
    from app.models.study_assistant import LectureNote
    from app.models.marketplace import MarketplaceItem
    from app.models.community import CampusClub, ClubMembership, CommunityPost, TeamRequest
    from app.models.facility import FacilityTicket

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="student", nullable=False)  # student, admin, campus_staff
    campus_name: Mapped[str] = mapped_column(String(120), default="Main Campus", index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Core Relationships
    profile: Mapped[Optional["StudentProfile"]] = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    assessment_attempts: Mapped[List["AssessmentAttempt"]] = relationship(
        "AssessmentAttempt",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    study_plans: Mapped[List["StudyPlan"]] = relationship(
        "StudyPlan",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    mock_interviews: Mapped[List["MockInterview"]] = relationship(
        "MockInterview",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Opportunity Relationships
    saved_opportunities: Mapped[List["SavedOpportunity"]] = relationship(
        "SavedOpportunity",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    applications: Mapped[List["ApplicationTracking"]] = relationship(
        "ApplicationTracking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Campus Super-App Pillar Relationships
    lecture_notes: Mapped[List["LectureNote"]] = relationship(
        "LectureNote",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    marketplace_items: Mapped[List["MarketplaceItem"]] = relationship(
        "MarketplaceItem",
        back_populates="seller",
        cascade="all, delete-orphan"
    )
    clubs_led: Mapped[List["CampusClub"]] = relationship(
        "CampusClub",
        back_populates="lead_user",
        foreign_keys="CampusClub.lead_user_id"
    )
    club_memberships: Mapped[List["ClubMembership"]] = relationship(
        "ClubMembership",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    community_posts: Mapped[List["CommunityPost"]] = relationship(
        "CommunityPost",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    team_requests: Mapped[List["TeamRequest"]] = relationship(
        "TeamRequest",
        back_populates="creator",
        cascade="all, delete-orphan"
    )
    facility_tickets: Mapped[List["FacilityTicket"]] = relationship(
        "FacilityTicket",
        back_populates="reporter",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}' role='{self.role}'>"


class StudentProfile(Base, TimestampMixin):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False
    )
    degree: Mapped[str] = mapped_column(String(100), nullable=False)  # B.Tech, B.E., M.Tech, BCA
    branch: Mapped[str] = mapped_column(String(100), nullable=False)  # Computer Science, IT, ECE, EEE
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    cgpa: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    target_roles: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    preferred_locations: Mapped[Optional[list]] = mapped_column(JSON, default=list, nullable=True)
    prep_hours_week: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    hostel_block: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    room_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<StudentProfile user_id={self.user_id} branch='{self.branch}' grad_year={self.graduation_year}>"
