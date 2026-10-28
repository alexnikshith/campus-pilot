from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class CampusClub(Base):
    __tablename__ = "campus_clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lead_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    campus_name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(
        String(60),
        default="coding",
        index=True,
        nullable=False
    )  # coding, robotics, ai, cultural, design, entrepreneurship
    description: Mapped[str] = mapped_column(Text, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    is_official: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    lead_user: Mapped["User"] = relationship("User", back_populates="clubs_led", foreign_keys=[lead_user_id])
    memberships: Mapped[List["ClubMembership"]] = relationship(
        "ClubMembership",
        back_populates="club",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CampusClub id={self.id} name='{self.name}' campus='{self.campus_name}'>"


class ClubMembership(Base):
    __tablename__ = "club_memberships"
    __table_args__ = (
        UniqueConstraint("club_id", "user_id", name="uq_club_user_membership"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    club_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("campus_clubs.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    role: Mapped[str] = mapped_column(String(40), default="member", nullable=False)  # member, coordinator, lead
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    club: Mapped["CampusClub"] = relationship("CampusClub", back_populates="memberships")
    user: Mapped["User"] = relationship("User", back_populates="club_memberships")


class CommunityPost(Base, TimestampMixin):
    __tablename__ = "community_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    campus_name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    post_type: Mapped[str] = mapped_column(
        String(50),
        default="project_showcase",
        index=True,
        nullable=False
    )  # project_showcase, idea, event_announcement, general
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="community_posts")

    def __repr__(self) -> str:
        return f"<CommunityPost id={self.id} title='{self.title}' type='{self.post_type}'>"


class TeamRequest(Base, TimestampMixin):
    __tablename__ = "team_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    campus_name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    event_or_project_name: Mapped[str] = mapped_column(String(180), nullable=False)
    roles_needed: Mapped[list] = mapped_column(JSON, default=list, nullable=False)  # ['Frontend', 'Backend']
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        index=True,
        nullable=False
    )  # open, filled, closed

    creator: Mapped["User"] = relationship("User", back_populates="team_requests")

    def __repr__(self) -> str:
        return f"<TeamRequest id={self.id} event='{self.event_or_project_name}' status='{self.status}'>"
