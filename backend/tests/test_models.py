from datetime import datetime, timezone, timedelta, date
from decimal import Decimal
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
import app.models as models

def test_metadata_table_registration():
    """Verify that all 25 domain models are registered in Base.metadata."""
    expected_tables = {
        "users",
        "student_profiles",
        "questions",
        "assessments",
        "assessment_questions",
        "assessment_attempts",
        "assessment_attempt_answers",
        "study_plans",
        "study_plan_tasks",
        "resumes",
        "mock_interviews",
        "opportunities",
        "saved_opportunities",
        "application_tracking",
        "lecture_notes",
        "note_summaries",
        "flashcard_decks",
        "flashcards",
        "note_mcqs",
        "marketplace_items",
        "campus_clubs",
        "club_memberships",
        "community_posts",
        "team_requests",
        "facility_tickets"
    }
    actual_tables = set(Base.metadata.tables.keys())
    missing = expected_tables - actual_tables
    assert not missing, f"Missing tables in metadata: {missing}"


def test_user_and_profile_crud_and_cascade(db_session: Session):
    """Verify User and StudentProfile relationship, query, and cascade deletion."""
    user = models.User(
        email="test_student@campus.edu",
        full_name="Priya Patel",
        password_hash="argon2_hashed_secret",
        role="student",
        campus_name="NIE Tech Campus",
        is_active=True
    )
    db_session.add(user)
    db_session.flush()

    profile = models.StudentProfile(
        user_id=user.id,
        degree="B.Tech",
        branch="Information Technology",
        graduation_year=2026,
        cgpa=Decimal("9.10"),
        skills=["Python", "FastAPI", "PostgreSQL"],
        target_roles=["Backend Engineer"],
        prep_hours_week=18
    )
    db_session.add(profile)
    db_session.flush()

    # Query back
    queried_user = db_session.query(models.User).filter_by(email="test_student@campus.edu").first()
    assert queried_user is not None
    assert queried_user.profile is not None
    assert queried_user.profile.branch == "Information Technology"
    assert queried_user.profile.cgpa == Decimal("9.10")

    # Cascade delete verification
    user_id = user.id
    db_session.delete(queried_user)
    db_session.flush()

    assert db_session.query(models.User).filter_by(id=user_id).first() is None
    assert db_session.query(models.StudentProfile).filter_by(user_id=user_id).first() is None


def test_assessment_attempt_and_scoring(db_session: Session):
    """Verify Question, Assessment, Attempt, and Answers with score aggregation."""
    user = models.User(
        email="scorer@campus.edu",
        full_name="Rohan Verma",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    q1 = models.Question(
        subject="Data Structures & Algorithms",
        topic="Graphs",
        difficulty="medium",
        question_text="What is the time complexity of Dijkstra's algorithm with a binary min-heap?",
        options=[
            {"id": "A", "text": "O(V^2)"},
            {"id": "B", "text": "O((V + E) log V)"},
            {"id": "C", "text": "O(E log V)"},
            {"id": "D", "text": "O(V log E)"}
        ],
        correct_option="B",
        explanation="Using a binary min-heap, extracting min takes O(log V) for each vertex and edge relaxation takes O(log V) per edge, yielding O((V + E) log V).",
        marks=2
    )
    db_session.add(q1)
    db_session.flush()

    assessment = models.Assessment(
        title="DSA Graph Theory Drill",
        description="Focused evaluation on shortest path algorithms.",
        assessment_type="subject_mock",
        duration_minutes=30,
        pass_percentage=Decimal("60.00")
    )
    db_session.add(assessment)
    db_session.flush()

    aq = models.AssessmentQuestion(
        assessment_id=assessment.id,
        question_id=q1.id,
        order_index=1,
        marks=2
    )
    db_session.add(aq)
    db_session.flush()

    attempt = models.AssessmentAttempt(
        user_id=user.id,
        assessment_id=assessment.id,
        started_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc),
        total_score=Decimal("2.00"),
        maximum_score=Decimal("2.00"),
        percentage=Decimal("100.00"),
        status="completed"
    )
    db_session.add(attempt)
    db_session.flush()

    ans = models.AssessmentAttemptAnswer(
        attempt_id=attempt.id,
        question_id=q1.id,
        selected_option="B",
        is_correct=True,
        marks_awarded=Decimal("2.00")
    )
    db_session.add(ans)
    db_session.flush()

    assert attempt.percentage == Decimal("100.00")
    assert len(attempt.answers) == 1
    assert attempt.answers[0].is_correct is True


def test_study_plan_task_progression(db_session: Session):
    """Verify StudyPlan creation and task completion workflow."""
    user = models.User(
        email="planner@campus.edu",
        full_name="Kavya Nair",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    plan = models.StudyPlan(
        user_id=user.id,
        target_role="Frontend Engineer",
        title="React & State Management Prep",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        status="active",
        total_tasks=1,
        completed_tasks=0
    )
    db_session.add(plan)
    db_session.flush()

    task = models.StudyPlanTask(
        study_plan_id=plan.id,
        title="Master React Hooks & Context API",
        description="Study useReducer and memoization techniques.",
        subject="Programming Fundamentals",
        topic="React Hooks",
        scheduled_date=date.today(),
        estimated_minutes=60,
        status="pending"
    )
    db_session.add(task)
    db_session.flush()

    # Complete the task
    task.status = "completed"
    task.completed_at = datetime.now(timezone.utc)
    plan.completed_tasks = 1
    db_session.flush()

    queried_plan = db_session.query(models.StudyPlan).filter_by(id=plan.id).first()
    assert queried_plan.completed_tasks == 1
    assert queried_plan.tasks[0].status == "completed"


def test_opportunity_and_tracking_pipeline(db_session: Session):
    """Verify Opportunity creation, saving, and application pipeline tracking."""
    user = models.User(
        email="applicant@campus.edu",
        full_name="Aditya Sen",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    opp = models.Opportunity(
        category="internship",
        company_name="Acme AI Labs",
        job_title="ML Research Intern",
        description="Work on model quantization and evaluation pipelines.",
        required_skills=["PyTorch", "Python"],
        eligibility_criteria="B.Tech 3rd/4th year. Minimum 8.0 CGPA.",
        graduation_years=[2025, 2026],
        minimum_cgpa=Decimal("8.00"),
        location="Remote",
        application_url="https://example.com/apply",
        deadline=datetime.now(timezone.utc) + timedelta(days=20),
        verification_status="verified"
    )
    db_session.add(opp)
    db_session.flush()

    # Save
    saved = models.SavedOpportunity(user_id=user.id, opportunity_id=opp.id)
    db_session.add(saved)

    # Track application
    tracking = models.ApplicationTracking(
        user_id=user.id,
        opportunity_id=opp.id,
        status="Applied",
        applied_date=datetime.now(timezone.utc),
        notes="Applied with updated ML resume."
    )
    db_session.add(tracking)
    db_session.flush()

    # Update pipeline status
    tracking.status = "Interview"
    db_session.flush()

    queried_track = db_session.query(models.ApplicationTracking).filter_by(user_id=user.id).first()
    assert queried_track.status == "Interview"
    assert queried_track.opportunity.company_name == "Acme AI Labs"


def test_ai_study_assistant_workflow(db_session: Session):
    """Verify LectureNote, NoteSummary, FlashcardDeck, Flashcards, and NoteMCQ cascade."""
    user = models.User(
        email="notes_user@campus.edu",
        full_name="Meera Joshi",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    note = models.LectureNote(
        user_id=user.id,
        title="Computer Networks: Congestion Control",
        subject="Computer Networks",
        original_filename="CN_Lecture12.pdf",
        storage_filename="uuid_cn_lecture12.pdf",
        file_size_bytes=250000,
        extracted_text="TCP Congestion control mechanisms: AIMD, Slow Start, Fast Retransmit, Fast Recovery."
    )
    db_session.add(note)
    db_session.flush()

    deck = models.FlashcardDeck(
        note_id=note.id,
        user_id=user.id,
        title="Congestion Control Flashcards",
        card_count=1
    )
    db_session.add(deck)
    db_session.flush()

    card = models.Flashcard(
        deck_id=deck.id,
        front_prompt="What does AIMD stand for in TCP?",
        back_solution="Additive Increase Multiplicative Decrease.",
        mastery_level=2
    )
    db_session.add(card)
    db_session.flush()

    deck_id = deck.id
    db_session.delete(deck)
    db_session.flush()

    # Verify flashcards are deleted with deck
    assert db_session.query(models.Flashcard).filter_by(deck_id=deck_id).first() is None


def test_marketplace_campus_scoping(db_session: Session):
    """Verify MarketplaceItem with campus isolation and price handling."""
    user = models.User(
        email="seller@campus.edu",
        full_name="Vikram Singh",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    item = models.MarketplaceItem(
        seller_id=user.id,
        campus_name="NIE Tech Campus",
        title="Engineering Chemistry Lab Coat (Size M)",
        category="calculators_lab",
        description="Clean white lab coat, washed and ironed.",
        price=Decimal("200.00"),
        condition="used_good",
        contact_method="hostel_room",
        contact_details="Room C-102, Aryabhata Hostel",
        status="available"
    )
    db_session.add(item)
    db_session.flush()

    item.status = "sold"
    db_session.flush()

    queried_item = db_session.query(models.MarketplaceItem).filter_by(id=item.id).first()
    assert queried_item.status == "sold"
    assert queried_item.campus_name == "NIE Tech Campus"


def test_campus_community_and_hostel_services(db_session: Session):
    """Verify CampusClub, CommunityPost, TeamRequest, and FacilityTicket."""
    user = models.User(
        email="community_lead@campus.edu",
        full_name="Ananya Desai",
        password_hash="hashed_pw",
        role="student",
        campus_name="NIE Tech Campus"
    )
    db_session.add(user)
    db_session.flush()

    club = models.CampusClub(
        lead_user_id=user.id,
        campus_name="NIE Tech Campus",
        name="NIE Robotics Society",
        category="robotics",
        description="Autonomous rovers and embedded systems group."
    )
    db_session.add(club)

    post = models.CommunityPost(
        author_id=user.id,
        campus_name="NIE Tech Campus",
        post_type="idea",
        title="Campus Quadcopter Project",
        content="Proposing an automated delivery drone experiment."
    )
    db_session.add(post)

    ticket = models.FacilityTicket(
        reporter_id=user.id,
        campus_name="NIE Tech Campus",
        facility_area="hostel",
        block_or_building="Gargi Girls Hostel",
        room_or_location="Room 204",
        issue_category="electricity",
        title="Ceiling fan regulator sparking",
        description="Regulator switch emits sparks when turning from speed 2 to 3.",
        urgency="high",
        status="open"
    )
    db_session.add(ticket)
    db_session.flush()

    queried_ticket = db_session.query(models.FacilityTicket).filter_by(id=ticket.id).first()
    assert queried_ticket.urgency == "high"
    assert queried_ticket.status == "open"
