import pytest
from decimal import Decimal
from fastapi.testclient import TestClient


def register_and_login(client: TestClient, email: str, role: str = "student", campus_name: str = "Apex Institute of Technology"):
    """Helper to register and login a user and return the auth headers and user ID."""
    reg_resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Password@1234",
            "full_name": "Test User",
            "campus_name": campus_name,
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


def test_get_profile_taxonomy(client: TestClient):
    """Test retrieving standard catalogs for skills, branches, roles, and hostel blocks."""
    resp = client.get("/api/v1/profile/taxonomy")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    data = body["data"]

    assert "degrees" in data
    assert "B.Tech" in data["degrees"]

    assert "branches" in data
    assert "Computer Science and Engineering" in data["branches"]

    assert "skills_by_category" in data
    assert len(data["skills_by_category"]) >= 5
    first_cat = data["skills_by_category"][0]
    assert "category" in first_cat
    assert "items" in first_cat

    assert "target_roles" in data
    assert "Software Development Engineer (SDE)" in data["target_roles"]

    assert "hostel_blocks" in data
    assert "Aryabhatta Block" in data["hostel_blocks"]


def test_get_current_profile_success(client: TestClient):
    """Test retrieving the logged-in student's academic profile and completeness breakdown."""
    headers, user_id = register_and_login(client, "student1@apex.edu")

    resp = client.get("/api/v1/profile", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True

    profile = body["data"]
    assert profile["user_id"] == user_id
    assert profile["degree"] == "B.Tech"
    assert profile["branch"] == "Computer Science and Engineering"
    assert profile["graduation_year"] == 2026
    assert "completeness" in profile
    assert 0 <= profile["completeness"]["total_percentage"] <= 100


def test_update_student_profile(client: TestClient):
    """Test updating academic fields, skills, target roles, and living details."""
    headers, user_id = register_and_login(client, "student2@apex.edu")

    update_payload = {
        "degree": "B.Tech",
        "branch": "Information Technology",
        "graduation_year": 2027,
        "cgpa": 8.75,
        "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
        "target_roles": ["Backend Developer", "Cloud & DevOps Engineer"],
        "preferred_locations": ["Bangalore", "Hyderabad"],
        "prep_hours_week": 20,
        "hostel_block": "Aryabhatta Block",
        "room_number": "304",
        "phone_number": "+91 9876543210",
        "bio": "Aspiring backend developer focused on high-scale systems."
    }

    put_resp = client.put("/api/v1/profile", headers=headers, json=update_payload)
    assert put_resp.status_code == 200
    body = put_resp.json()
    assert body["success"] is True

    data = body["data"]
    assert data["branch"] == "Information Technology"
    assert data["graduation_year"] == 2027
    assert float(data["cgpa"]) == 8.75
    assert len(data["skills"]) == 5
    assert "FastAPI" in data["skills"]
    assert len(data["target_roles"]) == 2
    assert data["hostel_block"] == "Aryabhatta Block"
    assert data["room_number"] == "304"
    assert data["completeness"]["total_percentage"] == 100


def test_update_profile_invalid_cgpa_fails(client: TestClient):
    """Test that CGPA > 10.00 or < 0.00 fails validation."""
    headers, _ = register_and_login(client, "student3@apex.edu")

    # CGPA > 10.00
    resp = client.put("/api/v1/profile", headers=headers, json={"cgpa": 11.50})
    assert resp.status_code == 422
    assert resp.json()["success"] is False

    # CGPA < 0.00
    resp2 = client.put("/api/v1/profile", headers=headers, json={"cgpa": -1.00})
    assert resp2.status_code == 422
    assert resp2.json()["success"] is False


def test_profile_completeness_calculation(client: TestClient):
    """Test detailed breakdown of completeness scores across all 5 dimensions."""
    headers, _ = register_and_login(client, "student4@apex.edu")

    resp = client.get("/api/v1/profile/completeness", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True

    comp = body["data"]
    assert "total_percentage" in comp
    assert "basic_info" in comp
    assert "academic_info" in comp
    assert "target_roles" in comp
    assert "skills" in comp
    assert "hostel_info" in comp
    assert "missing_fields" in comp
    assert "next_step_recommendation" in comp


def test_onboarding_wizard_submission(client: TestClient):
    """Test completing the multi-step onboarding wizard in a single call."""
    headers, _ = register_and_login(client, "onboarding_student@apex.edu")

    onboarding_data = {
        "degree": "B.Tech",
        "branch": "Computer Science and Engineering",
        "graduation_year": 2026,
        "cgpa": 9.10,
        "skills": ["Java", "Spring Boot", "Data Structures & Algorithms", "SQL", "Docker"],
        "target_roles": ["Software Development Engineer (SDE)", "Backend Developer"],
        "preferred_locations": ["Bangalore", "Pune"],
        "prep_hours_week": 18,
        "hostel_block": "Bhaskara Block",
        "room_number": "212",
        "phone_number": "+91 9988776655",
        "bio": "Competitive programmer and Java backend developer."
    }

    resp = client.post("/api/v1/profile/onboarding", headers=headers, json=onboarding_data)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True

    data = body["data"]
    assert data["degree"] == "B.Tech"
    assert float(data["cgpa"]) == 9.10
    assert "Java" in data["skills"]
    assert data["completeness"]["total_percentage"] == 100


def test_onboarding_requires_skills_and_roles(client: TestClient):
    """Test that onboarding rejects submissions with empty skills or empty target roles."""
    headers, _ = register_and_login(client, "student_empty@apex.edu")

    # Empty skills
    resp = client.post(
        "/api/v1/profile/onboarding",
        headers=headers,
        json={
            "degree": "B.Tech",
            "branch": "Computer Science and Engineering",
            "graduation_year": 2026,
            "skills": [],
            "target_roles": ["Software Development Engineer (SDE)"]
        }
    )
    assert resp.status_code == 422

    # Empty target roles
    resp2 = client.post(
        "/api/v1/profile/onboarding",
        headers=headers,
        json={
            "degree": "B.Tech",
            "branch": "Computer Science and Engineering",
            "graduation_year": 2026,
            "skills": ["Python"],
            "target_roles": []
        }
    )
    assert resp2.status_code == 422


def test_student_cannot_view_peer_profile(client: TestClient):
    """Test that student A cannot access student B's profile via /{user_id}."""
    headers_a, id_a = register_and_login(client, "student_a@apex.edu")
    _, id_b = register_and_login(client, "student_b@apex.edu")

    # Student A tries to view Student B's profile
    resp = client.get(f"/api/v1/profile/{id_b}", headers=headers_a)
    assert resp.status_code == 403
    assert resp.json()["success"] is False
    assert "denied" in resp.json()["error"]["message"].lower() or "ownership" in resp.json()["error"]["message"].lower()


def test_admin_can_view_any_student_profile(client: TestClient):
    """Test that an administrator or campus staff can view any student's profile."""
    # Register student
    _, student_id = register_and_login(client, "student_target@apex.edu", role="student")

    # Register staff
    headers_staff, _ = register_and_login(client, "staff_member@apex.edu", role="campus_staff")

    resp = client.get(f"/api/v1/profile/{student_id}", headers=headers_staff)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["user_id"] == student_id


def test_unauthenticated_profile_access_fails(client: TestClient):
    """Test that accessing profile endpoints without token returns 401."""
    resp = client.get("/api/v1/profile")
    assert resp.status_code == 401
    assert resp.json()["success"] is False

