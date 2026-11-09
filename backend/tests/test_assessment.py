from datetime import datetime, timezone
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.assessment import Question, Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAttemptAnswer
from app.models.user import User


def register_and_login(client: TestClient, email: str, role: str = "student"):
    """Helper to register and login a user and return the auth headers and user ID."""
    reg_resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Password@1234",
            "full_name": f"User {email}",
            "campus_name": "Apex Institute of Technology",
            "role": role,
            "degree": "B.Tech",
            "branch": "Computer Science and Engineering",
            "graduation_year": 2026,
        }
    )
    assert reg_resp.status_code == 201

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password@1234"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["data"]["access_token"]
    user_id = login_resp.json()["data"]["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


def seed_test_assessment(db: Session) -> Assessment:
    """Helper to seed questions and an assessment across multiple subjects."""
    now = datetime.now(timezone.utc)

    q1 = Question(
        subject="Data Structures & Algorithms",
        topic="Binary Search Trees",
        difficulty="medium",
        question_text="What is the worst-case search complexity of an unbalanced BST?",
        question_type="mcq",
        options=[
            {"id": "A", "text": "O(1)"},
            {"id": "B", "text": "O(log n)"},
            {"id": "C", "text": "O(n)"},
            {"id": "D", "text": "O(n log n)"}
        ],
        correct_option="C",
        explanation="In an unbalanced BST degenerated into a linked list, traversal is O(n).",
        marks=2,
        is_active=True,
        created_at=now
    )
    q2 = Question(
        subject="Operating Systems",
        topic="Deadlocks",
        difficulty="hard",
        question_text="Which of the following is NOT one of Coffman's four deadlock conditions?",
        question_type="mcq",
        options=[
            {"id": "A", "text": "Mutual Exclusion"},
            {"id": "B", "text": "Preemption Allowed"},
            {"id": "C", "text": "Hold and Wait"},
            {"id": "D", "text": "Circular Wait"}
        ],
        correct_option="B",
        explanation="No Preemption is the necessary condition. If preemption is allowed, deadlocks are broken.",
        marks=2,
        is_active=True,
        created_at=now
    )
    q3 = Question(
        subject="DBMS",
        topic="Normalization",
        difficulty="medium",
        question_text="For a relation to be in BCNF, every determinant must be a:",
        question_type="mcq",
        options=[
            {"id": "A", "text": "Foreign Key"},
            {"id": "B", "text": "Candidate Key / Super Key"},
            {"id": "C", "text": "Secondary Index"},
            {"id": "D", "text": "Composite Key"}
        ],
        correct_option="B",
        explanation="BCNF strictly mandates that determinant X in X -> Y must be a super key.",
        marks=1,
        is_active=True,
        created_at=now
    )
    db.add_all([q1, q2, q3])
    db.flush()

    assessment = Assessment(
        title="Diagnostic Placement Readiness Test",
        description="Comprehensive evaluation across DSA, OS, and DBMS.",
        assessment_type="diagnostic",
        duration_minutes=30,
        pass_percentage=Decimal("60.00"),
        is_active=True,
        created_at=now
    )
    db.add(assessment)
    db.flush()

    aq1 = AssessmentQuestion(assessment_id=assessment.id, question_id=q1.id, order_index=1, marks=2)
    aq2 = AssessmentQuestion(assessment_id=assessment.id, question_id=q2.id, order_index=2, marks=2)
    aq3 = AssessmentQuestion(assessment_id=assessment.id, question_id=q3.id, order_index=3, marks=1)
    db.add_all([aq1, aq2, aq3])
    db.commit()
    db.refresh(assessment)
    return assessment


def test_list_assessments(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student1@test.com")
    seed_test_assessment(db_session)

    resp = client.get("/api/v1/assessments", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1

    item = body["data"][0]
    assert item["title"] == "Diagnostic Placement Readiness Test"
    assert item["total_questions"] == 3
    assert item["total_marks"] == 5
    assert set(item["subjects"]) == {"Data Structures & Algorithms", "Operating Systems", "DBMS"}


def test_get_assessment_detail_masking(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student2@test.com")
    assessment = seed_test_assessment(db_session)

    resp = client.get(f"/api/v1/assessments/{assessment.id}", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    data = body["data"]

    assert len(data["questions"]) == 3
    for q in data["questions"]:
        # Verify strict masking of answers and technical explanations
        assert "correct_option" not in q
        assert "explanation" not in q
        assert "options" in q
        assert len(q["options"]) == 4


def test_start_assessment_attempt(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student3@test.com")
    assessment = seed_test_assessment(db_session)

    resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    data = body["data"]

    attempt_id = data["attempt_id"]
    assert attempt_id > 0
    assert data["assessment_id"] == assessment.id
    assert data["duration_minutes"] == 30
    assert "expires_at" in data
    assert len(data["questions"]) == 3

    # Ensure questions during test do not leak correct options or explanations
    for q in data["questions"]:
        assert "correct_option" not in q
        assert "explanation" not in q

    # Starting again while still in time resumes the same attempt
    resp2 = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    assert resp2.status_code == 201
    assert resp2.json()["data"]["attempt_id"] == attempt_id


def test_submit_assessment_perfect_score(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student4@test.com")
    assessment = seed_test_assessment(db_session)

    # 1. Start attempt
    start_resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    attempt_id = start_resp.json()["data"]["attempt_id"]
    questions = start_resp.json()["data"]["questions"]

    # 2. Submit all correct answers (C for q1, B for q2, B for q3)
    answers = [
        {"question_id": questions[0]["id"], "selected_option": "C"},
        {"question_id": questions[1]["id"], "selected_option": "B"},
        {"question_id": questions[2]["id"], "selected_option": "B"}
    ]

    submit_resp = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": answers},
        headers=headers
    )
    assert submit_resp.status_code == 200
    body = submit_resp.json()
    assert body["success"] is True
    data = body["data"]

    assert float(data["total_score"]) == 5.0
    assert float(data["maximum_score"]) == 5.0
    assert float(data["percentage"]) == 100.0
    assert data["passed"] is True
    assert data["status"] == "completed"

    # All subjects should be proficient
    breakdown = data["subject_breakdown"]
    assert breakdown["Data Structures & Algorithms"]["status"] == "proficient"
    assert breakdown["Operating Systems"]["status"] == "proficient"
    assert breakdown["DBMS"]["status"] == "proficient"

    # Post-submission review now exposes explanations and correct options
    assert len(data["answers"]) == 3
    for ans in data["answers"]:
        assert "correct_option" in ans
        assert "explanation" in ans
        assert ans["is_correct"] is True
        assert float(ans["marks_awarded"]) > 0


def test_submit_assessment_partial_score_and_diagnostics(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student5@test.com")
    assessment = seed_test_assessment(db_session)

    start_resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    attempt_id = start_resp.json()["data"]["attempt_id"]
    questions = start_resp.json()["data"]["questions"]

    # q1 correct (2 marks), q2 wrong (0 marks), q3 left blank (0 marks)
    answers = [
        {"question_id": questions[0]["id"], "selected_option": "C"},
        {"question_id": questions[1]["id"], "selected_option": "A"},  # Wrong (correct is B)
        # q3 omitted
    ]

    submit_resp = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": answers},
        headers=headers
    )
    assert submit_resp.status_code == 200
    data = submit_resp.json()["data"]

    assert float(data["total_score"]) == 2.0
    assert float(data["maximum_score"]) == 5.0
    assert float(data["percentage"]) == 40.0
    assert data["passed"] is False

    # Diagnostic checks
    breakdown = data["subject_breakdown"]
    assert breakdown["Data Structures & Algorithms"]["status"] == "proficient"
    assert breakdown["Operating Systems"]["status"] == "needs_focus"
    assert "Deadlocks" in breakdown["Operating Systems"]["topics_needing_work"]
    assert breakdown["DBMS"]["status"] == "needs_focus"

    assert "Operating Systems" in data["weaknesses"]
    assert len(data["recommendations"]) >= 1


def test_prevent_duplicate_submit(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student6@test.com")
    assessment = seed_test_assessment(db_session)

    start_resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    attempt_id = start_resp.json()["data"]["attempt_id"]

    submit_resp = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": []},
        headers=headers
    )
    assert submit_resp.status_code == 200

    # Second submit must be rejected
    dup_resp = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": []},
        headers=headers
    )
    assert dup_resp.status_code == 400
    assert "already been submitted" in dup_resp.json()["error"]["message"]


def test_authorization_and_privacy(client: TestClient, db_session: Session):
    student_headers, _ = register_and_login(client, "student7a@test.com")
    other_headers, _ = register_and_login(client, "student7b@test.com")
    staff_headers, _ = register_and_login(client, "staff@test.com", role="campus_staff")

    assessment = seed_test_assessment(db_session)
    start_resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=student_headers)
    attempt_id = start_resp.json()["data"]["attempt_id"]

    # Other student cannot submit
    tamper_resp = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": []},
        headers=other_headers
    )
    assert tamper_resp.status_code == 403

    # Submit legitimately by owner
    client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": []},
        headers=student_headers
    )

    # Other student cannot view results
    view_other = client.get(f"/api/v1/assessments/attempts/{attempt_id}/results", headers=other_headers)
    assert view_other.status_code == 403

    # Campus staff CAN view results
    view_staff = client.get(f"/api/v1/assessments/attempts/{attempt_id}/results", headers=staff_headers)
    assert view_staff.status_code == 200
    assert view_staff.json()["data"]["attempt_id"] == attempt_id


def test_assessment_history_and_overview_stats(client: TestClient, db_session: Session):
    headers, _ = register_and_login(client, "student8@test.com")
    assessment = seed_test_assessment(db_session)

    # Initially empty history and stats
    stats_empty = client.get("/api/v1/assessments/stats", headers=headers).json()["data"]
    assert stats_empty["total_attempts"] == 0
    assert float(stats_empty["average_score_percentage"]) == 0.0

    # Start and submit attempt
    start_resp = client.post(f"/api/v1/assessments/{assessment.id}/start", headers=headers)
    attempt_id = start_resp.json()["data"]["attempt_id"]
    questions = start_resp.json()["data"]["questions"]

    # Submit 2 correct answers (4 marks / 5 = 80%)
    client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json={"answers": [
            {"question_id": questions[0]["id"], "selected_option": "C"},
            {"question_id": questions[1]["id"], "selected_option": "B"}
        ]},
        headers=headers
    )

    # Check history
    hist_resp = client.get("/api/v1/assessments/history", headers=headers)
    assert hist_resp.status_code == 200
    hist = hist_resp.json()["data"]
    assert len(hist) == 1
    assert hist[0]["id"] == attempt_id
    assert float(hist[0]["percentage"]) == 80.0
    assert hist[0]["passed"] is True

    # Check stats
    stats_resp = client.get("/api/v1/assessments/stats", headers=headers)
    assert stats_resp.status_code == 200
    stats = stats_resp.json()["data"]
    assert stats["total_attempts"] == 1
    assert stats["completed_attempts"] == 1
    assert float(stats["average_score_percentage"]) == 80.0
    assert stats["best_subject"] is not None
