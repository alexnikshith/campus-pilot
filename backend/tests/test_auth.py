from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.core.rate_limiter import auth_rate_limiter

@pytest.fixture(autouse=True)
def clean_rate_limiter():
    """Ensure rate limiter state is reset before every test."""
    auth_rate_limiter.clear_all()
    yield
    auth_rate_limiter.clear_all()


def test_registration_success(client: TestClient, db_session: Session):
    """Test successful student registration and automatic profile linkage."""
    payload = {
        "email": "student_alpha@campus.edu",
        "full_name": "Rohan Deshmukh",
        "password": "StrongPassword2026!",
        "campus_name": "National Institute of Engineering (NIE)",
        "degree": "B.Tech",
        "branch": "Computer Science and Engineering",
        "graduation_year": 2026
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "student_alpha@campus.edu"
    assert data["data"]["full_name"] == "Rohan Deshmukh"
    assert data["data"]["role"] == "student"
    assert "password_hash" not in data["data"]

    # Verify database state
    user_in_db = db_session.query(User).filter_by(email="student_alpha@campus.edu").first()
    assert user_in_db is not None
    assert user_in_db.profile is not None
    assert user_in_db.profile.branch == "Computer Science and Engineering"


def test_registration_duplicate_email_fails(client: TestClient):
    """Test that registering with an existing email returns 409 Conflict."""
    payload = {
        "email": "duplicate_user@campus.edu",
        "full_name": "Original User",
        "password": "StrongPassword2026!",
        "campus_name": "NIE Tech Campus"
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409
    data = res2.json()
    assert data["success"] is False
    assert data["error"]["code"] == "RESOURCE_CONFLICT"
    assert "already registered" in data["error"]["message"]


def test_registration_weak_password_fails(client: TestClient):
    """Test password complexity rejection (422 Unprocessable Entity)."""
    # 1. Too short
    res_short = client.post("/api/v1/auth/register", json={
        "email": "weak1@campus.edu",
        "full_name": "Weak User",
        "password": "Aa1!"
    })
    assert res_short.status_code == 422

    # 2. No special character
    res_no_sym = client.post("/api/v1/auth/register", json={
        "email": "weak2@campus.edu",
        "full_name": "Weak User",
        "password": "Password123"
    })
    assert res_no_sym.status_code == 422

    # 3. No uppercase
    res_no_upper = client.post("/api/v1/auth/register", json={
        "email": "weak3@campus.edu",
        "full_name": "Weak User",
        "password": "password123!"
    })
    assert res_no_upper.status_code == 422


def test_registration_admin_self_assignment_fails(client: TestClient):
    """Verify that users cannot self-register with an admin role."""
    payload = {
        "email": "rogue_admin@campus.edu",
        "full_name": "Rogue Admin",
        "password": "StrongPassword2026!",
        "role": "admin"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    assert "Administrative roles cannot be self-assigned" in str(response.json())


def test_login_success(client: TestClient, db_session: Session):
    """Test successful authentication returning Bearer token and user response."""
    # Seed user directly
    user = User(
        email="login_user@campus.edu",
        full_name="Meera Sen",
        password_hash=get_password_hash("LoginPassword2026!"),
        role="student",
        campus_name="NIE Tech Campus",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    login_res = client.post("/api/v1/auth/login", json={
        "email": "login_user@campus.edu",
        "password": "LoginPassword2026!"
    })
    assert login_res.status_code == 200
    payload = login_res.json()
    assert payload["success"] is True
    assert "access_token" in payload["data"]
    assert payload["data"]["token_type"] == "bearer"
    assert payload["data"]["expires_in"] > 0
    assert payload["data"]["user"]["email"] == "login_user@campus.edu"


def test_login_invalid_password_fails(client: TestClient, db_session: Session):
    """Test authentication failure with incorrect password returns 401."""
    user = User(
        email="badpass_user@campus.edu",
        full_name="User",
        password_hash=get_password_hash("CorrectPass2026!"),
        role="student",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    login_res = client.post("/api/v1/auth/login", json={
        "email": "badpass_user@campus.edu",
        "password": "WrongPassword2026!"
    })
    assert login_res.status_code == 401
    assert login_res.json()["error"]["code"] == "UNAUTHORIZED"
    assert "Invalid email address or password" in login_res.json()["error"]["message"]


def test_login_nonexistent_email_fails(client: TestClient):
    """Test authentication failure with non-existent email returns same safe error."""
    login_res = client.post("/api/v1/auth/login", json={
        "email": "ghost_user@campus.edu",
        "password": "AnyPassword2026!"
    })
    assert login_res.status_code == 401
    assert "Invalid email address or password" in login_res.json()["error"]["message"]


def test_login_inactive_user_fails(client: TestClient, db_session: Session):
    """Test suspended/inactive user account cannot authenticate."""
    user = User(
        email="suspended@campus.edu",
        full_name="Suspended User",
        password_hash=get_password_hash("StrongPass2026!"),
        role="student",
        is_active=False
    )
    db_session.add(user)
    db_session.commit()

    login_res = client.post("/api/v1/auth/login", json={
        "email": "suspended@campus.edu",
        "password": "StrongPass2026!"
    })
    assert login_res.status_code == 401
    assert "suspended or deactivated" in login_res.json()["error"]["message"]


def test_get_current_user_profile(client: TestClient, db_session: Session):
    """Test retrieval of current user and profile via Bearer token."""
    user = User(
        email="me_endpoint@campus.edu",
        full_name="Aarav Rao",
        password_hash=get_password_hash("Pass2026!Strong"),
        role="student",
        campus_name="NIE Tech Campus",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(subject=user.id, claims={"email": user.email, "role": user.role})
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["user"]["email"] == "me_endpoint@campus.edu"
    assert payload["data"]["user"]["full_name"] == "Aarav Rao"


def test_token_validation_errors(client: TestClient, db_session: Session):
    """Test expired, malformed, and missing token scenarios."""
    user = User(
        email="token_test@campus.edu",
        full_name="Token Tester",
        password_hash=get_password_hash("Pass2026!Strong"),
        role="student",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    # 1. Missing header
    res_missing = client.get("/api/v1/auth/me")
    assert res_missing.status_code == 401
    assert "Authentication credentials required" in res_missing.json()["error"]["message"]

    # 2. Malformed token
    res_malformed = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer not-a-valid-jwt"})
    assert res_malformed.status_code == 401
    assert "Malformed or invalid token" in res_malformed.json()["error"]["message"]

    # 3. Expired token
    expired_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(seconds=-10)  # Created in the past
    )
    res_expired = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res_expired.status_code == 401
    assert "token has expired" in res_expired.json()["error"]["message"]


def test_update_current_user_profile(client: TestClient, db_session: Session):
    """Test updating user account details via PUT /auth/me."""
    user = User(
        email="update_me@campus.edu",
        full_name="Original Name",
        password_hash=get_password_hash("Pass2026!Strong"),
        role="student",
        campus_name="Old Campus",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(subject=user.id)
    response = client.put(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Name", "campus_name": "New Campus"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == "Updated Name"
    assert response.json()["data"]["campus_name"] == "New Campus"


def test_password_change_workflow(client: TestClient, db_session: Session):
    """Test password change validation, execution, and subsequent login with new password."""
    user = User(
        email="pwchange@campus.edu",
        full_name="Password Changer",
        password_hash=get_password_hash("OldPassword2026!"),
        role="student",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(subject=user.id)

    # 1. Wrong current password
    res_wrong = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": "WrongCurrentPassword!", "new_password": "NewStrongPass2026!"}
    )
    assert res_wrong.status_code == 401
    assert "Current password is incorrect" in res_wrong.json()["error"]["message"]

    # 2. Same new password
    res_same = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": "OldPassword2026!", "new_password": "OldPassword2026!"}
    )
    assert res_same.status_code == 400
    assert "must be different" in res_same.json()["error"]["message"]

    # 3. Successful change
    res_success = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": "OldPassword2026!", "new_password": "BrandNewPass2026!"}
    )
    assert res_success.status_code == 200
    assert res_success.json()["data"]["updated"] is True

    # 4. Old password no longer works
    res_old_login = client.post("/api/v1/auth/login", json={
        "email": "pwchange@campus.edu",
        "password": "OldPassword2026!"
    })
    assert res_old_login.status_code == 401

    # 5. New password authenticates cleanly
    res_new_login = client.post("/api/v1/auth/login", json={
        "email": "pwchange@campus.edu",
        "password": "BrandNewPass2026!"
    })
    assert res_new_login.status_code == 200


def test_role_based_access_control(client: TestClient, db_session: Session):
    """Test RBAC route guards: students blocked with 403, administrators allowed."""
    student = User(
        email="student_guard@campus.edu",
        full_name="Student Guard",
        password_hash="hash",
        role="student",
        is_active=True
    )
    admin = User(
        email="admin_guard@campus.edu",
        full_name="Admin Guard",
        password_hash="hash",
        role="admin",
        is_active=True
    )
    db_session.add_all([student, admin])
    db_session.commit()

    student_token = create_access_token(subject=student.id)
    admin_token = create_access_token(subject=admin.id)

    # Student accessing admin endpoint -> 403 Forbidden
    res_forbidden = client.get(
        "/api/v1/auth/admin-check",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert res_forbidden.status_code == 403
    assert res_forbidden.json()["error"]["code"] == "FORBIDDEN"
    assert "requires one of the following roles: admin" in res_forbidden.json()["error"]["message"]

    # Admin accessing admin endpoint -> 200 OK
    res_allowed = client.get(
        "/api/v1/auth/admin-check",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res_allowed.status_code == 200
    assert res_allowed.json()["data"]["role"] == "admin"


def test_student_resource_ownership(client: TestClient, db_session: Session):
    """Test student isolation boundary: student A cannot access student B's data, but admin can."""
    student_a = User(
        email="student_a@campus.edu",
        full_name="Student A",
        password_hash="hash",
        role="student",
        is_active=True
    )
    student_b = User(
        email="student_b@campus.edu",
        full_name="Student B",
        password_hash="hash",
        role="student",
        is_active=True
    )
    admin = User(
        email="dean@campus.edu",
        full_name="Dean",
        password_hash="hash",
        role="admin",
        is_active=True
    )
    db_session.add_all([student_a, student_b, admin])
    db_session.commit()

    token_a = create_access_token(subject=student_a.id)
    token_b = create_access_token(subject=student_b.id)
    token_admin = create_access_token(subject=admin.id)

    # 1. Student A accessing their own data -> 200 OK
    res_own = client.get(
        f"/api/v1/auth/student-private-data/{student_a.id}",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert res_own.status_code == 200
    assert res_own.json()["data"]["accessed_user_id"] == student_a.id

    # 2. Student A accessing Student B's data -> 403 Forbidden
    res_cross = client.get(
        f"/api/v1/auth/student-private-data/{student_b.id}",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert res_cross.status_code == 403
    assert "another student's private data" in res_cross.json()["error"]["message"]

    # 3. Admin accessing Student B's data -> 200 OK
    res_admin = client.get(
        f"/api/v1/auth/student-private-data/{student_b.id}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert res_admin.status_code == 200
    assert res_admin.json()["data"]["accessed_user_id"] == student_b.id


def test_login_rate_limiting(client: TestClient, db_session: Session):
    """Test that 5 consecutive failed login attempts trigger 429 Too Many Requests."""
    user = User(
        email="brute_victim@campus.edu",
        full_name="Victim",
        password_hash=get_password_hash("Password123!"),
        role="student",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    # 5 failed attempts
    for _ in range(5):
        res = client.post("/api/v1/auth/login", json={
            "email": "brute_victim@campus.edu",
            "password": "WrongPassword!"
        })
        assert res.status_code == 401

    # 6th attempt triggers Rate Limit lockout (429)
    res_locked = client.post("/api/v1/auth/login", json={
        "email": "brute_victim@campus.edu",
        "password": "Password123!"  # Even if password is right now, account is locked
    })
    assert res_locked.status_code == 429
    assert res_locked.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"
    assert "Temporarily locked for security" in res_locked.json()["error"]["message"]


def test_logout_endpoint(client: TestClient, db_session: Session):
    """Test logout endpoint confirms session closure."""
    user = User(
        email="logout_user@campus.edu",
        full_name="Logout User",
        password_hash=get_password_hash("Password123!"),
        role="student",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(subject=user.id)
    response = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["logged_out"] is True

