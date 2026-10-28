from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Numeric, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class MockInterview(Base):
    __tablename__ = "mock_interviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    role: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    # Technical Fundamentals, Programming, DBMS, Operating Systems, Computer Networks, Behavioral
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    student_answer: Mapped[str] = mapped_column(Text, nullable=False)
    technical_accuracy_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    clarity_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    completeness_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    overall_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True)
    evaluation_rubric: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    feedback_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_ai_evaluated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="mock_interviews")

    def __repr__(self) -> str:
        return f"<MockInterview id={self.id} role='{self.role}' category='{self.category}'>"
