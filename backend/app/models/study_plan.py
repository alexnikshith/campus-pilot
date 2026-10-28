from datetime import datetime, timezone, date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, ForeignKey, JSON, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class StudyPlan(Base, TimestampMixin):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    target_role: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)  # active, completed, archived
    total_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    recommendation_rules: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="study_plans")
    tasks: Mapped[List["StudyPlanTask"]] = relationship(
        "StudyPlanTask",
        back_populates="study_plan",
        cascade="all, delete-orphan",
        order_by="StudyPlanTask.scheduled_date"
    )

    def __repr__(self) -> str:
        return f"<StudyPlan id={self.id} user_id={self.user_id} title='{self.title}'>"


class StudyPlanTask(Base):
    __tablename__ = "study_plan_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    study_plan_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("study_plans.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    scheduled_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=45, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True, nullable=False)  # pending, completed
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    study_plan: Mapped["StudyPlan"] = relationship("StudyPlan", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<StudyPlanTask id={self.id} topic='{self.topic}' status='{self.status}'>"
