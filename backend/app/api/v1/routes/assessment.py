from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_active_user
from app.schemas.common import ResponseEnvelope
from app.schemas.assessment import (
    AssessmentSummaryResponse,
    AssessmentDetailResponse,
    StartAttemptResponse,
    SubmitAttemptRequest,
    AttemptResultResponse,
    AttemptHistoryItem,
    AssessmentOverviewStats,
)
from app.services.assessment_service import assessment_service

router = APIRouter(prefix="/assessments", tags=["Placement Readiness Assessments"])


@router.get(
    "",
    response_model=ResponseEnvelope[List[AssessmentSummaryResponse]],
    summary="List active assessments",
    description="Retrieve catalog of technical diagnostic and mock assessments with question count and subject tags."
)
def list_assessments(
    assessment_type: Optional[str] = Query(None, description="Filter by type (diagnostic, subject_mock, company_mock)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assessments = assessment_service.list_assessments(db, assessment_type=assessment_type)
    return ResponseEnvelope(
        success=True,
        data=assessments,
        message="Active assessments retrieved successfully"
    )


@router.get(
    "/stats",
    response_model=ResponseEnvelope[AssessmentOverviewStats],
    summary="Get user assessment overview stats",
    description="Aggregated placement readiness performance metrics including total tests, average score, and focus areas."
)
def get_user_assessment_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    stats = assessment_service.get_user_stats(db, current_user)
    return ResponseEnvelope(
        success=True,
        data=stats,
        message="Assessment overview statistics retrieved successfully"
    )


@router.get(
    "/history",
    response_model=ResponseEnvelope[List[AttemptHistoryItem]],
    summary="Get user assessment history",
    description="Retrieve all past and active assessment attempts for the authenticated student."
)
def get_assessment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    history = assessment_service.get_user_history(db, current_user)
    return ResponseEnvelope(
        success=True,
        data=history,
        message="Assessment attempt history retrieved successfully"
    )


@router.get(
    "/{assessment_id}",
    response_model=ResponseEnvelope[AssessmentDetailResponse],
    summary="Get assessment details",
    description="Retrieve assessment overview and question sequence with answers/explanations strictly masked."
)
def get_assessment_detail(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    detail = assessment_service.get_assessment_detail(db, assessment_id)
    return ResponseEnvelope(
        success=True,
        data=detail,
        message="Assessment details retrieved successfully"
    )


@router.post(
    "/{assessment_id}/start",
    response_model=ResponseEnvelope[StartAttemptResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Start or resume a timed assessment attempt",
    description="Creates or resumes a server-timed assessment session. Masks correct answers and explanations."
)
def start_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    attempt = assessment_service.start_assessment(db, assessment_id, current_user)
    return ResponseEnvelope(
        success=True,
        data=attempt,
        message="Assessment attempt started successfully"
    )


@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=ResponseEnvelope[AttemptResultResponse],
    summary="Submit assessment answers",
    description="Scores the submitted answers server-side, generates subject diagnostic breakdown, and returns complete result report."
)
def submit_assessment(
    attempt_id: int,
    submission: SubmitAttemptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = assessment_service.submit_assessment(db, attempt_id, current_user, submission)
    return ResponseEnvelope(
        success=True,
        data=result,
        message="Assessment submitted and scored successfully"
    )


@router.get(
    "/attempts/{attempt_id}/results",
    response_model=ResponseEnvelope[AttemptResultResponse],
    summary="Get attempt scorecard & review",
    description="Retrieve full scorecard, weakness diagnostic breakdown, and question-by-question review with explanations."
)
def get_attempt_results(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = assessment_service.get_attempt_result(db, attempt_id, current_user)
    return ResponseEnvelope(
        success=True,
        data=result,
        message="Assessment results retrieved successfully"
    )
