from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any
from app.core.config import settings
from app.db.session import check_db_connection

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
    database: Dict[str, Any]

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def get_health() -> HealthResponse:
    """
    Application health-check endpoint.
    Reports operational status and database reachability without exposing infrastructure secrets.
    """
    db_ok, db_message = check_db_connection()
    
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        app=settings.APP_NAME,
        environment=settings.APP_ENV,
        database={
            "connected": db_ok,
            "message": db_message
        }
    )
