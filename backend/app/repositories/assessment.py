from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, desc

from app.models.assessment import (
    Assessment,
    Question,
    AssessmentQuestion,
    AssessmentAttempt,
    AssessmentAttemptAnswer,
)
from app.repositories.base import BaseRepository
from app.core.exceptions import EntityNotFoundException, BadRequestException


class AssessmentRepository(BaseRepository[Assessment, Any, Any]):
    def __init__(self):
        super().__init__(Assessment)

    def get_active_assessments(
        self,
        db: Session,
        assessment_type: Optional[str] = None
    ) -> List[Assessment]:
        """Fetch all active assessments with ordered questions eagerly loaded."""
        stmt = (
            select(Assessment)
            .options(
                joinedload(Assessment.assessment_questions).joinedload(AssessmentQuestion.question)
            )
            .where(Assessment.is_active == True)
        )
        if assessment_type:
            stmt = stmt.where(Assessment.assessment_type == assessment_type)
        stmt = stmt.order_by(Assessment.id.asc())
        return list(db.scalars(stmt).unique().all())

    def get_assessment_with_questions(
        self,
        db: Session,
        assessment_id: int
    ) -> Optional[Assessment]:
        """Fetch an assessment by ID with ordered questions and question details."""
        stmt = (
            select(Assessment)
            .options(
                joinedload(Assessment.assessment_questions).joinedload(AssessmentQuestion.question)
            )
            .where(Assessment.id == assessment_id)
        )
        return db.scalars(stmt).unique().first()

    def get_active_attempt(
        self,
        db: Session,
        user_id: int,
        assessment_id: int
    ) -> Optional[AssessmentAttempt]:
        """Find an in-progress attempt for this user and assessment."""
        stmt = (
            select(AssessmentAttempt)
            .where(
                AssessmentAttempt.user_id == user_id,
                AssessmentAttempt.assessment_id == assessment_id,
                AssessmentAttempt.status == "in_progress"
            )
            .order_by(AssessmentAttempt.started_at.desc())
        )
        return db.scalars(stmt).first()

    def create_attempt(
        self,
        db: Session,
        user_id: int,
        assessment_id: int
    ) -> AssessmentAttempt:
        """Create a new in-progress assessment attempt."""
        now = datetime.now(timezone.utc)
        attempt = AssessmentAttempt(
            user_id=user_id,
            assessment_id=assessment_id,
            started_at=now,
            status="in_progress",
            total_score=Decimal("0.00"),
            maximum_score=Decimal("0.00"),
            percentage=Decimal("0.00")
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    def get_attempt_with_details(
        self,
        db: Session,
        attempt_id: int
    ) -> Optional[AssessmentAttempt]:
        """Fetch attempt with assessment and recorded answers eagerly loaded."""
        stmt = (
            select(AssessmentAttempt)
            .options(
                joinedload(AssessmentAttempt.assessment),
                joinedload(AssessmentAttempt.answers).joinedload(AssessmentAttemptAnswer.question)
            )
            .where(AssessmentAttempt.id == attempt_id)
        )
        return db.scalars(stmt).unique().first()

    def get_user_attempts_history(
        self,
        db: Session,
        user_id: int
    ) -> List[AssessmentAttempt]:
        """Fetch all assessment attempts for a user ordered from newest to oldest."""
        stmt = (
            select(AssessmentAttempt)
            .options(joinedload(AssessmentAttempt.assessment))
            .where(AssessmentAttempt.user_id == user_id)
            .order_by(AssessmentAttempt.started_at.desc())
        )
        return list(db.scalars(stmt).all())

    def get_user_stats(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """Compute aggregated statistics for a user's completed assessments."""
        attempts = (
            db.scalars(
                select(AssessmentAttempt)
                .where(
                    AssessmentAttempt.user_id == user_id,
                    AssessmentAttempt.status == "completed"
                )
            )
            .all()
        )

        total_attempts = len(attempts)
        if total_attempts == 0:
            return {
                "total_attempts": 0,
                "completed_attempts": 0,
                "average_score_percentage": Decimal("0.00"),
                "best_subject": None,
                "focus_area": None
            }

        avg_pct = sum(a.percentage for a in attempts) / Decimal(str(total_attempts))

        # Aggregate subject performance across all completed attempts
        subject_scores: Dict[str, Dict[str, Decimal]] = {}
        for a in attempts:
            if a.subject_breakdown and isinstance(a.subject_breakdown, dict):
                for subj, data in a.subject_breakdown.items():
                    if subj not in subject_scores:
                        subject_scores[subj] = {"score": Decimal("0.0"), "max": Decimal("0.0")}
                    score_val = Decimal(str(data.get("score", 0)))
                    max_val = Decimal(str(data.get("max", 0)))
                    subject_scores[subj]["score"] += score_val
                    subject_scores[subj]["max"] += max_val

        best_subject = None
        focus_area = None
        highest_pct = Decimal("-1.0")
        lowest_pct = Decimal("101.0")

        for subj, totals in subject_scores.items():
            if totals["max"] > 0:
                pct = (totals["score"] / totals["max"]) * Decimal("100.00")
                if pct > highest_pct:
                    highest_pct = pct
                    best_subject = subj
                if pct < lowest_pct:
                    lowest_pct = pct
                    focus_area = subj

        return {
            "total_attempts": total_attempts,
            "completed_attempts": total_attempts,
            "average_score_percentage": round(avg_pct, 2),
            "best_subject": best_subject,
            "focus_area": focus_area
        }


assessment_repository = AssessmentRepository()

