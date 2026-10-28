from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class FacilityTicket(Base):
    __tablename__ = "facility_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    reporter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    campus_name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    facility_area: Mapped[str] = mapped_column(
        String(80),
        default="hostel",
        index=True,
        nullable=False
    )  # hostel, academic_block, lab, cafeteria, sports
    block_or_building: Mapped[str] = mapped_column(String(100), nullable=False)
    room_or_location: Mapped[str] = mapped_column(String(100), nullable=False)
    issue_category: Mapped[str] = mapped_column(
        String(60),
        index=True,
        nullable=False
    )  # water, electricity, internet_wifi, carpentry, cleanliness
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(
        String(20),
        default="medium",
        nullable=False
    )  # low, medium, high, emergency
    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        index=True,
        nullable=False
    )  # open, acknowledged, in_progress, resolved, rejected
    assigned_staff: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    reporter: Mapped["User"] = relationship("User", back_populates="facility_tickets")

    def __repr__(self) -> str:
        return f"<FacilityTicket id={self.id} title='{self.title}' status='{self.status}' campus='{self.campus_name}'>"
