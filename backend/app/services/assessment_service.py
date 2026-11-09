from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.assessment import (
    Assessment,
    Question,
    AssessmentQuestion,
    AssessmentAttempt,
    AssessmentAttemptAnswer,
)
from app.repositories.assessment import assessment_repository
from app.schemas.assessment import (
    QuestionPublicResponse,
    QuestionReviewResponse,
    AssessmentSummaryResponse,
    AssessmentDetailResponse,
    StartAttemptResponse,
    SubmitAttemptRequest,
    SubjectScoreDetail,
    AttemptResultResponse,
    AttemptHistoryItem,
    AssessmentOverviewStats,
)
from app.core.exceptions import EntityNotFoundException, BadRequestException, ForbiddenException


class AssessmentService:
    def __init__(self, repo=assessment_repository):
        self.repo = repo

    def list_assessments(
        self,
        db: Session,
        assessment_type: Optional[str] = None
    ) -> List[AssessmentSummaryResponse]:
        """Fetch active assessments summarized with question counts and covered subjects."""
        assessments = self.repo.get_active_assessments(db, assessment_type=assessment_type)
        results: List[AssessmentSummaryResponse] = []

        for a in assessments:
            questions = [aq.question for aq in a.assessment_questions if aq.question and aq.question.is_active]
            total_marks = sum(aq.marks for aq in a.assessment_questions)
            subjects = list(dict.fromkeys(q.subject for q in questions))

            results.append(
                AssessmentSummaryResponse(
                    id=a.id,
                    title=a.title,
                    description=a.description,
                    assessment_type=a.assessment_type,
                    duration_minutes=a.duration_minutes,
                    pass_percentage=a.pass_percentage,
                    total_questions=len(questions),
                    total_marks=total_marks,
                    subjects=subjects,
                    is_active=a.is_active,
                    created_at=a.created_at
                )
            )
        return results

    def get_assessment_detail(
        self,
        db: Session,
        assessment_id: int
    ) -> AssessmentDetailResponse:
        """Fetch assessment details with public question data (no answers/explanations)."""
        assessment = self.repo.get_assessment_with_questions(db, assessment_id)
        if not assessment or not assessment.is_active:
            raise EntityNotFoundException(entity_name="Assessment", identifier=assessment_id)

        ordered_aqs = sorted(assessment.assessment_questions, key=lambda x: x.order_index)
        public_questions: List[QuestionPublicResponse] = []
        subjects: List[str] = []

        for aq in ordered_aqs:
            q = aq.question
            if q and q.is_active:
                if q.subject not in subjects:
                    subjects.append(q.subject)
                public_questions.append(
                    QuestionPublicResponse(
                        id=q.id,
                        subject=q.subject,
                        topic=q.topic,
                        difficulty=q.difficulty,
                        question_text=q.question_text,
                        question_type=q.question_type,
                        options=q.options,
                        marks=aq.marks
                    )
                )

        total_marks = sum(q.marks for q in public_questions)

        return AssessmentDetailResponse(
            id=assessment.id,
            title=assessment.title,
            description=assessment.description,
            assessment_type=assessment.assessment_type,
            duration_minutes=assessment.duration_minutes,
            pass_percentage=assessment.pass_percentage,
            total_questions=len(public_questions),
            total_marks=total_marks,
            subjects=subjects,
            is_active=assessment.is_active,
            created_at=assessment.created_at,
            questions=public_questions
        )

    def start_assessment(
        self,
        db: Session,
        assessment_id: int,
        current_user: User
    ) -> StartAttemptResponse:
        """
        Initiate or resume a timed assessment attempt.
        Masks all correct options and technical explanations.
        """
        assessment = self.repo.get_assessment_with_questions(db, assessment_id)
        if not assessment or not assessment.is_active:
            raise EntityNotFoundException(entity_name="Assessment", identifier=assessment_id)

        now = datetime.now(timezone.utc)
        active_attempt = self.repo.get_active_attempt(db, current_user.id, assessment_id)

        if active_attempt:
            # Check if previous attempt has expired with grace period
            duration_delta = timedelta(minutes=assessment.duration_minutes)
            started_at = active_attempt.started_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=timezone.utc)

            time_elapsed = now - started_at
            if time_elapsed <= (duration_delta + timedelta(minutes=2)):
                # Resume current valid attempt
                attempt = active_attempt
            else:
                # Expire previous attempt and create new attempt
                active_attempt.status = "expired"
                active_attempt.submitted_at = started_at + duration_delta
                db.commit()
                attempt = self.repo.create_attempt(db, current_user.id, assessment_id)
        else:
            attempt = self.repo.create_attempt(db, current_user.id, assessment_id)

        started_at = attempt.started_at
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)
        expires_at = started_at + timedelta(minutes=assessment.duration_minutes)

        ordered_aqs = sorted(assessment.assessment_questions, key=lambda x: x.order_index)
        questions: List[QuestionPublicResponse] = []
        for aq in ordered_aqs:
            q = aq.question
            if q and q.is_active:
                questions.append(
                    QuestionPublicResponse(
                        id=q.id,
                        subject=q.subject,
                        topic=q.topic,
                        difficulty=q.difficulty,
                        question_text=q.question_text,
                        question_type=q.question_type,
                        options=q.options,
                        marks=aq.marks
                    )
                )

        return StartAttemptResponse(
            attempt_id=attempt.id,
            assessment_id=assessment.id,
            assessment_title=assessment.title,
            duration_minutes=assessment.duration_minutes,
            started_at=started_at,
            expires_at=expires_at,
            total_questions=len(questions),
            questions=questions
        )

    def submit_assessment(
        self,
        db: Session,
        attempt_id: int,
        current_user: User,
        submission: SubmitAttemptRequest
    ) -> AttemptResultResponse:
        """
        Submit answers for an assessment attempt, perform server-side scoring,
        and generate diagnostic breakdown with weakness recommendations.
        """
        attempt = self.repo.get_attempt_with_details(db, attempt_id)
        if not attempt:
            raise EntityNotFoundException(entity_name="AssessmentAttempt", identifier=attempt_id)

        if attempt.user_id != current_user.id and current_user.role not in ("admin", "campus_staff"):
            raise ForbiddenException("You cannot submit an assessment attempt for another user.")

        if attempt.status == "completed":
            raise BadRequestException("This assessment attempt has already been submitted and scored.")

        assessment = self.repo.get_assessment_with_questions(db, attempt.assessment_id)
        if not assessment:
            raise EntityNotFoundException(entity_name="Assessment", identifier=attempt.assessment_id)

        now = datetime.now(timezone.utc)
        attempt.submitted_at = now
        attempt.status = "completed"

        # Map submissions by question_id
        answers_map = {ans.question_id: (ans.selected_option.strip() if ans.selected_option else None) for ans in submission.answers}

        # Clear any prior recorded answers on this attempt (if partial)
        for existing_ans in list(attempt.answers):
            db.delete(existing_ans)
        db.flush()

        total_score = Decimal("0.00")
        max_score = Decimal("0.00")
        subject_agg: Dict[str, Dict[str, Any]] = {}
        ordered_aqs = sorted(assessment.assessment_questions, key=lambda x: x.order_index)

        review_answers: List[QuestionReviewResponse] = []

        for aq in ordered_aqs:
            q = aq.question
            if not q:
                continue

            q_marks = Decimal(str(aq.marks))
            max_score += q_marks

            subj = q.subject
            if subj not in subject_agg:
                subject_agg[subj] = {
                    "score": Decimal("0.00"),
                    "max": Decimal("0.00"),
                    "topics_needing_work": set()
                }
            subject_agg[subj]["max"] += q_marks

            selected_opt = answers_map.get(q.id)
            is_correct = False
            awarded = Decimal("0.00")

            if selected_opt:
                if selected_opt.upper() == q.correct_option.strip().upper():
                    is_correct = True
                    awarded = q_marks
                    total_score += awarded
                    subject_agg[subj]["score"] += awarded
                else:
                    subject_agg[subj]["topics_needing_work"].add(q.topic)
            else:
                # Unanswered counts as topic needing work
                subject_agg[subj]["topics_needing_work"].add(q.topic)

            # Record answer record
            ans_record = AssessmentAttemptAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                selected_option=selected_opt,
                is_correct=is_correct,
                marks_awarded=awarded
            )
            db.add(ans_record)

            review_answers.append(
                QuestionReviewResponse(
                    id=q.id,
                    subject=q.subject,
                    topic=q.topic,
                    difficulty=q.difficulty,
                    question_text=q.question_text,
                    question_type=q.question_type,
                    options=q.options,
                    correct_option=q.correct_option,
                    explanation=q.explanation,
                    marks=aq.marks,
                    selected_option=selected_opt,
                    is_correct=is_correct,
                    marks_awarded=awarded
                )
            )

        # Compute percentage
        percentage = Decimal("0.00")
        if max_score > Decimal("0.00"):
            percentage = round((total_score / max_score) * Decimal("100.00"), 2)

        attempt.total_score = total_score
        attempt.maximum_score = max_score
        attempt.percentage = percentage

        # Build subject breakdown dictionary for persistence & response
        subject_breakdown: Dict[str, SubjectScoreDetail] = {}
        strengths: List[str] = []
        weaknesses: List[str] = []
        recommendations: List[str] = []

        for subj, data in subject_agg.items():
            subj_score = data["score"]
            subj_max = data["max"]
            subj_pct = Decimal("0.00")
            if subj_max > Decimal("0.00"):
                subj_pct = round((subj_score / subj_max) * Decimal("100.00"), 2)

            if subj_pct >= Decimal("75.00"):
                subj_status = "proficient"
                strengths.append(subj)
            elif subj_pct >= Decimal("50.00"):
                subj_status = "competent"
            else:
                subj_status = "needs_focus"
                weaknesses.append(subj)

            topics_work = sorted(list(data["topics_needing_work"]))
            if subj_status == "needs_focus":
                recommendations.append(
                    f"Prioritize foundational revision in {subj}, especially topics: {', '.join(topics_work[:3])}."
                )

            subject_breakdown[subj] = SubjectScoreDetail(
                score=subj_score,
                max=subj_max,
                percentage=subj_pct,
                status=subj_status,
                topics_needing_work=topics_work
            )

        if not recommendations:
            recommendations.append(
                "Great work! Maintain consistency across coding exercises and company-specific mock tests."
            )

        # Store JSON breakdown in attempt
        attempt.subject_breakdown = {
            subj: {
                "score": float(item.score),
                "max": float(item.max),
                "percentage": float(item.percentage),
                "status": item.status,
                "topics_needing_work": item.topics_needing_work
            }
            for subj, item in subject_breakdown.items()
        }

        db.commit()
        db.refresh(attempt)

        started_at = attempt.started_at
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)

        duration_taken = int((now - started_at).total_seconds())

        return AttemptResultResponse(
            attempt_id=attempt.id,
            assessment_id=assessment.id,
            assessment_title=assessment.title,
            started_at=started_at,
            submitted_at=now,
            duration_seconds_taken=duration_taken,
            total_score=total_score,
            maximum_score=max_score,
            percentage=percentage,
            passed=(percentage >= assessment.pass_percentage),
            pass_percentage=assessment.pass_percentage,
            status=attempt.status,
            subject_breakdown=subject_breakdown,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            answers=review_answers
        )

    def get_attempt_result(
        self,
        db: Session,
        attempt_id: int,
        current_user: User
    ) -> AttemptResultResponse:
        """Fetch completed assessment scorecard and comprehensive question review."""
        attempt = self.repo.get_attempt_with_details(db, attempt_id)
        if not attempt:
            raise EntityNotFoundException(entity_name="AssessmentAttempt", identifier=attempt_id)

        if attempt.user_id != current_user.id and current_user.role not in ("admin", "campus_staff"):
            raise ForbiddenException("You cannot view results for another student's assessment attempt.")

        if attempt.status != "completed":
            raise BadRequestException(f"Assessment attempt status is '{attempt.status}'. Complete and submit to review results.")

        assessment = self.repo.get_assessment_with_questions(db, attempt.assessment_id)
        if not assessment:
            raise EntityNotFoundException(entity_name="Assessment", identifier=attempt.assessment_id)

        # Map answers
        answers_by_qid = {ans.question_id: ans for ans in attempt.answers}
        ordered_aqs = sorted(assessment.assessment_questions, key=lambda x: x.order_index)

        review_answers: List[QuestionReviewResponse] = []
        for aq in ordered_aqs:
            q = aq.question
            if not q:
                continue
            recorded = answers_by_qid.get(q.id)
            review_answers.append(
                QuestionReviewResponse(
                    id=q.id,
                    subject=q.subject,
                    topic=q.topic,
                    difficulty=q.difficulty,
                    question_text=q.question_text,
                    question_type=q.question_type,
                    options=q.options,
                    correct_option=q.correct_option,
                    explanation=q.explanation,
                    marks=aq.marks,
                    selected_option=recorded.selected_option if recorded else None,
                    is_correct=recorded.is_correct if recorded else False,
                    marks_awarded=recorded.marks_awarded if recorded else Decimal("0.00")
                )
            )

        # Parse stored subject breakdown
        subject_breakdown: Dict[str, SubjectScoreDetail] = {}
        strengths: List[str] = []
        weaknesses: List[str] = []
        recommendations: List[str] = []

        if attempt.subject_breakdown and isinstance(attempt.subject_breakdown, dict):
            for subj, data in attempt.subject_breakdown.items():
                pct = Decimal(str(data.get("percentage", 0)))
                status = data.get("status", "needs_focus")
                topics = data.get("topics_needing_work", [])

                if status == "proficient":
                    strengths.append(subj)
                elif status == "needs_focus":
                    weaknesses.append(subj)
                    recommendations.append(
                        f"Targeted review required for {subj} ({', '.join(topics[:3])})."
                    )

                subject_breakdown[subj] = SubjectScoreDetail(
                    score=Decimal(str(data.get("score", 0))),
                    max=Decimal(str(data.get("max", 0))),
                    percentage=pct,
                    status=status,
                    topics_needing_work=topics
                )

        if not recommendations:
            recommendations.append("Solid diagnostic baseline! Advance to subject mock drills.")

        started_at = attempt.started_at
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)

        duration_taken = None
        if attempt.submitted_at:
            submitted_at = attempt.submitted_at
            if submitted_at.tzinfo is None:
                submitted_at = submitted_at.replace(tzinfo=timezone.utc)
            duration_taken = int((submitted_at - started_at).total_seconds())

        return AttemptResultResponse(
            attempt_id=attempt.id,
            assessment_id=assessment.id,
            assessment_title=assessment.title,
            started_at=started_at,
            submitted_at=attempt.submitted_at,
            duration_seconds_taken=duration_taken,
            total_score=attempt.total_score,
            maximum_score=attempt.maximum_score,
            percentage=attempt.percentage,
            passed=(attempt.percentage >= assessment.pass_percentage),
            pass_percentage=assessment.pass_percentage,
            status=attempt.status,
            subject_breakdown=subject_breakdown,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            answers=review_answers
        )

    def get_user_history(
        self,
        db: Session,
        current_user: User
    ) -> List[AttemptHistoryItem]:
        """Fetch list of user's past assessment attempts."""
        attempts = self.repo.get_user_attempts_history(db, current_user.id)
        results: List[AttemptHistoryItem] = []

        for a in attempts:
            pass_pct = a.assessment.pass_percentage if a.assessment else Decimal("50.00")
            results.append(
                AttemptHistoryItem(
                    id=a.id,
                    assessment_id=a.assessment_id,
                    assessment_title=a.assessment.title if a.assessment else "Assessment",
                    assessment_type=a.assessment.assessment_type if a.assessment else "diagnostic",
                    started_at=a.started_at,
                    submitted_at=a.submitted_at,
                    total_score=a.total_score,
                    maximum_score=a.maximum_score,
                    percentage=a.percentage,
                    passed=(a.percentage >= pass_pct),
                    pass_percentage=pass_pct,
                    status=a.status
                )
            )
        return results

    def get_user_stats(
        self,
        db: Session,
        current_user: User
    ) -> AssessmentOverviewStats:
        """Fetch high-level overview metrics for the current user's assessment performance."""
        stats = self.repo.get_user_stats(db, current_user.id)
        return AssessmentOverviewStats(**stats)


assessment_service = AssessmentService()

