import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.user import User
from app.repositories.base import BaseRepository
from app.services.base import BaseService
from app.schemas.common import PaginationParams, PaginatedResponse
from app.core.exceptions import EntityNotFoundException

def test_response_envelope_format(client: TestClient):
    """Verify that successful endpoints return the standardized ResponseEnvelope."""
    response = client.get("/api/v1/system/echo?msg=HelloFoundation")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["message"] == "HelloFoundation"
    assert payload["data"]["category"] == "echo"
    assert "echoed successfully" in payload["message"]


def test_validation_error_handler(client: TestClient):
    """Verify that Pydantic validation failures return normalized ErrorEnvelope with field details."""
    # Message shorter than min_length (3)
    response = client.post("/api/v1/system/validate", json={"message": "a"})
    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert "Request validation failed" in payload["error"]["message"]
    assert isinstance(payload["error"]["details"], list)
    assert len(payload["error"]["details"]) > 0


def test_custom_exception_handlers(client: TestClient):
    """Verify centralized handling of custom domain exceptions (404, 409, 400)."""
    # 1. Not Found
    res_404 = client.get("/api/v1/system/trigger-error/not-found")
    assert res_404.status_code == 404
    data_404 = res_404.json()
    assert data_404["success"] is False
    assert data_404["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert "demo-999" in data_404["error"]["message"]

    # 2. Conflict
    res_409 = client.get("/api/v1/system/trigger-error/conflict")
    assert res_409.status_code == 409
    data_409 = res_409.json()
    assert data_409["success"] is False
    assert data_409["error"]["code"] == "RESOURCE_CONFLICT"

    # 3. Bad Request
    res_400 = client.get("/api/v1/system/trigger-error/bad-request")
    assert res_400.status_code == 400
    data_400 = res_400.json()
    assert data_400["success"] is False
    assert data_400["error"]["code"] == "BAD_REQUEST"


def test_pagination_engine_navigation_flags(client: TestClient):
    """Verify pagination metadata calculation on demo dataset (22 total items, 5 per page)."""
    # Page 1 (items 1-5 of 22)
    res_p1 = client.get("/api/v1/system/paginate-demo?page=1&page_size=5")
    assert res_p1.status_code == 200
    p1 = res_p1.json()["data"]
    assert p1["total"] == 22
    assert p1["total_pages"] == 5
    assert p1["page"] == 1
    assert p1["page_size"] == 5
    assert len(p1["items"]) == 5
    assert p1["has_next"] is True
    assert p1["has_prev"] is False

    # Page 5 (items 21-22 of 22)
    res_p5 = client.get("/api/v1/system/paginate-demo?page=5&page_size=5")
    assert res_p5.status_code == 200
    p5 = res_p5.json()["data"]
    assert p5["page"] == 5
    assert len(p5["items"]) == 2
    assert p5["has_next"] is False
    assert p5["has_prev"] is True


def test_telemetry_headers_and_request_id(client: TestClient):
    """Verify that X-Request-ID and X-Process-Time-Ms headers are injected on all responses."""
    custom_id = "test-custom-request-id-12345"
    response = client.get("/", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id
    assert "X-Process-Time-Ms" in response.headers
    process_time = float(response.headers["X-Process-Time-Ms"])
    assert process_time >= 0.0


def test_base_repository_crud(db_session: Session):
    """Verify BaseRepository CRUD operations and multi-entity pagination."""
    repo = BaseRepository[User, dict, dict](User)

    # 1. Create
    user = repo.create(db_session, obj_in={
        "email": "repo_test@campus.edu",
        "full_name": "Repo Tester",
        "password_hash": "hash123",
        "role": "student",
        "campus_name": "NIE Tech Campus"
    })
    assert user.id is not None
    assert user.email == "repo_test@campus.edu"

    # 2. Get and Get_or_404
    found = repo.get(db_session, user.id)
    assert found is not None
    assert found.full_name == "Repo Tester"

    found_strict = repo.get_or_404(db_session, user.id)
    assert found_strict.id == user.id

    # 3. Update
    updated = repo.update(db_session, db_obj=user, obj_in={"full_name": "Updated Repo Tester"})
    assert updated.full_name == "Updated Repo Tester"

    # 4. Multi query & Count
    items, total = repo.get_multi(db_session, skip=0, limit=10, sort_by="id", order="asc")
    assert total >= 1
    assert any(u.email == "repo_test@campus.edu" for u in items)

    count_all = repo.count(db_session)
    assert count_all == total

    # 5. Delete
    deleted = repo.delete(db_session, id=user.id)
    assert deleted is not None
    assert repo.get(db_session, user.id) is None

    # 6. Get_or_404 on deleted raises EntityNotFoundException
    with pytest.raises(EntityNotFoundException):
        repo.get_or_404(db_session, user.id)


def test_base_service_orchestration(db_session: Session):
    """Verify BaseService encapsulation of business methods with repository delegation."""
    repo = BaseRepository[User, dict, dict](User)
    service = BaseService[User, dict, dict, BaseRepository](repo)

    # Create via service
    user = service.create(db_session, obj_in={
        "email": "service_test@campus.edu",
        "full_name": "Service Tester",
        "password_hash": "secret",
        "role": "student",
        "campus_name": "NIE Tech Campus"
    })
    assert user.id is not None

    # Get Paginated via service
    pagination = PaginationParams(page=1, page_size=10)
    paginated = service.get_paginated(db_session, pagination=pagination)
    assert isinstance(paginated, PaginatedResponse)
    assert paginated.total >= 1
    assert any(u.email == "service_test@campus.edu" for u in paginated.items)

    # Cleanup
    service.delete(db_session, user.id)

