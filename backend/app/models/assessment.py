from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Numeric, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    # Subjects: Programming Fundamentals, DSA, DBMS, Operating Systems, Computer Networks, Aptitude
    topic: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)  # easy, medium, hard
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(30), default="mcq", nullable=False)
    options: Mapped[list] = mapped_column(JSON, nullable=False)  # [{'id': 'A', 'text': '...'}]
    correct_option: Mapped[str] = mapped_column(String(10), nullable=False)  # Hidden from student responses
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    marks: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    assessment_questions: Mapped[List["AssessmentQuestion"]] = relationship(
        "AssessmentQuestion",
        back_populates="question",
        cascade="all, delete-orphan"
    )
    attempt_answers: Mapped[List["AssessmentAttemptAnswer"]] = relationship(
        "AssessmentAttemptAnswer",
        back_populates="question"
    )

    def __repr__(self) -> str:
        return f"<Question id={self.id} subject='{self.subject}' topic='{self.topic}'>"


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(50), default="diagnostic", nullable=False)
    # diagnostic, subject_mock, company_mock
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    pass_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("50.00"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    assessment_questions: Mapped[List["AssessmentQuestion"]] = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan",
        order_by="AssessmentQuestion.order_index"
    )
    attempts: Mapped[List["AssessmentAttempt"]] = relationship(
        "AssessmentAttempt",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Assessment id={self.id} title='{self.title}'>"


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assessments.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    marks: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="assessment_questions")
    question: Mapped["Question"] = relationship("Question", back_populates="assessment_questions")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    assessment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assessments.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    maximum_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="in_progress", nullable=False)  # in_progress, completed, expired
    subject_breakdown: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="assessment_attempts")
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="attempts")
    answers: Mapped[List["AssessmentAttemptAnswer"]] = relationship(
        "AssessmentAttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AssessmentAttempt id={self.id} user_id={self.user_id} score={self.total_score}/{self.maximum_score}>"


class AssessmentAttemptAnswer(Base):
    __tablename__ = "assessment_attempt_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assessment_attempts.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    selected_option: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    marks_awarded: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)

    attempt: Mapped["AssessmentAttempt"] = relationship("AssessmentAttempt", back_populates="answers")
    question: Mapped["Question"] = relationship("Question", back_populates="attempt_answers")
