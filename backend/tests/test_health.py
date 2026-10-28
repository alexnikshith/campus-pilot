from unittest.mock import patch
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PlacementPilot"
    assert "/docs" in data["docs"]
    assert "/api/v1/health" in data["health"]

def test_health_endpoint_success(client: TestClient):
    with patch("app.api.v1.routes.health.check_db_connection", return_value=(True, "Database connection successful")):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "healthy"
        assert payload["app"] == "PlacementPilot"
        assert payload["database"]["connected"] is True
        assert "Database connection successful" in payload["database"]["message"]

def test_health_endpoint_degraded(client: TestClient):
    with patch("app.api.v1.routes.health.check_db_connection", return_value=(False, "Database connectivity unavailable (OperationalError)")):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "degraded"
        assert payload["database"]["connected"] is False
        assert "OperationalError" in payload["database"]["message"]
