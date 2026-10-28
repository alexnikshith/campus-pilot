"""
PlacementPilot & Campus Super-App SQLAlchemy 2.0 ORM Models
Aggregates and re-exports all domain entities for Alembic discovery and application use.
"""

from app.models.base import Base, TimestampMixin
from app.models.user import User, StudentProfile
from app.models.assessment import (
    Question,
    Assessment,
    AssessmentQuestion,
    AssessmentAttempt,
    AssessmentAttemptAnswer
)
from app.models.study_plan import StudyPlan, StudyPlanTask
from app.models.resume import Resume
from app.models.mock_interview import MockInterview
from app.models.opportunity import Opportunity, SavedOpportunity, ApplicationTracking
from app.models.study_assistant import (
    LectureNote,
    NoteSummary,
    FlashcardDeck,
    Flashcard,
    NoteMCQ
)
from app.models.marketplace import MarketplaceItem
from app.models.community import (
    CampusClub,
    ClubMembership,
    CommunityPost,
    TeamRequest
)
from app.models.facility import FacilityTicket

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "StudentProfile",
    "Question",
    "Assessment",
    "AssessmentQuestion",
    "AssessmentAttempt",
    "AssessmentAttemptAnswer",
    "StudyPlan",
    "StudyPlanTask",
    "Resume",
    "MockInterview",
    "Opportunity",
    "SavedOpportunity",
    "ApplicationTracking",
    "LectureNote",
    "NoteSummary",
    "FlashcardDeck",
    "Flashcard",
    "NoteMCQ",
    "MarketplaceItem",
    "CampusClub",
    "ClubMembership",
    "CommunityPost",
    "TeamRequest",
    "FacilityTicket",
]
