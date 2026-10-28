from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class Opportunity(Base, TimestampMixin):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    category: Mapped[str] = mapped_column(
        String(50),
        default="internship",
        index=True,
        nullable=False
    )  # job, internship, hackathon, competition, research, scholarship, placement_prep
    company_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    required_skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    eligibility_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    graduation_years: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    minimum_cgpa: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    location: Mapped[str] = mapped_column(String(120), default="Remote", nullable=False)
    prize_or_stipend: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    application_url: Mapped[str] = mapped_column(String(500), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    source: Mapped[str] = mapped_column(String(150), default="Verified Campus Board", nullable=False)
    verification_status: Mapped[str] = mapped_column(
        String(30),
        default="unverified",
        index=True,
        nullable=False
    )  # verified, unverified, expired

    saved_by_users: Mapped[List["SavedOpportunity"]] = relationship(
        "SavedOpportunity",
        back_populates="opportunity",
        cascade="all, delete-orphan"
    )
    applications: Mapped[List["ApplicationTracking"]] = relationship(
        "ApplicationTracking",
        back_populates="opportunity",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Opportunity id={self.id} title='{self.job_title}' company='{self.company_name}'>"


class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"
    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="uq_user_saved_opportunity"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    opportunity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="saved_opportunities")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="saved_by_users")


class ApplicationTracking(Base, TimestampMixin):
    __tablename__ = "application_tracking"
    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="uq_user_application_tracking"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    opportunity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(40),
        default="Interested",
        index=True,
        nullable=False
    )  # Interested, Applied, Shortlisted, Interview, Offer, Rejected, Withdrawn
    applied_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="applications")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="applications")

    def __repr__(self) -> str:
        return f"<ApplicationTracking user_id={self.user_id} opp_id={self.opportunity_id} status='{self.status}'>"
