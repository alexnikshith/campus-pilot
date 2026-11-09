from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class QuestionOption(BaseModel):
    id: str
    text: str


class QuestionPublicResponse(BaseModel):
    """Public question schema used during active timed assessments.
    Hidden fields: correct_option, explanation (never returned during exams).
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    topic: str
    difficulty: str
    question_text: str
    question_type: str = "mcq"
    options: List[Dict[str, Any]]
    marks: int = 1


class QuestionReviewResponse(BaseModel):
    """Detailed question schema for post-submission score review and feedback."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    topic: str
    difficulty: str
    question_text: str
    question_type: str = "mcq"
    options: List[Dict[str, Any]]
    correct_option: str
    explanation: str
    marks: int = 1
    selected_option: Optional[str] = None
    is_correct: Optional[bool] = None
    marks_awarded: Decimal = Decimal("0.00")


class AssessmentSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    assessment_type: str
    duration_minutes: int
    pass_percentage: Decimal
    total_questions: int
    total_marks: int
    subjects: List[str]
    is_active: bool = True
    created_at: datetime


class AssessmentDetailResponse(AssessmentSummaryResponse):
    questions: List[QuestionPublicResponse]


class StartAttemptResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    assessment_title: str
    duration_minutes: int
    started_at: datetime
    expires_at: datetime
    total_questions: int
    questions: List[QuestionPublicResponse]


class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: Optional[str] = Field(None, max_length=10)


class SubmitAttemptRequest(BaseModel):
    answers: List[AnswerSubmission] = Field(default_factory=list)


class SubjectScoreDetail(BaseModel):
    score: Decimal
    max: Decimal
    percentage: Decimal
    status: str  # proficient (>=75%), competent (>=50%), needs_focus (<50%)
    topics_needing_work: List[str] = Field(default_factory=list)


class AttemptResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attempt_id: int
    assessment_id: int
    assessment_title: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    duration_seconds_taken: Optional[int] = None
    total_score: Decimal
    maximum_score: Decimal
    percentage: Decimal
    passed: bool
    pass_percentage: Decimal
    status: str  # completed, in_progress, expired
    subject_breakdown: Dict[str, SubjectScoreDetail]
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    answers: List[QuestionReviewResponse] = Field(default_factory=list)


class AttemptHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assessment_id: int
    assessment_title: str
    assessment_type: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    total_score: Decimal
    maximum_score: Decimal
    percentage: Decimal
    passed: bool
    pass_percentage: Decimal
    status: str


class AssessmentOverviewStats(BaseModel):
    total_attempts: int = 0
    completed_attempts: int = 0
    average_score_percentage: Decimal = Decimal("0.00")
    best_subject: Optional[str] = None
    focus_area: Optional[str] = None
