from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from typing import Dict, Any
from app.core.config import settings
from app.db.session import check_db_connection

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    success: bool = Field(default=True, description="Request execution status")
    status: str = Field(description="System health status: healthy or degraded")
    app: str = Field(description="Application title")
    environment: str = Field(description="Runtime environment")
    database: Dict[str, Any] = Field(description="Database connectivity diagnostics")
    message: str = Field(default="Health check completed", description="Status message")

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def get_health() -> HealthResponse:
    """
    Application health-check endpoint.
    Reports operational status and database reachability without exposing infrastructure secrets.
    """
    db_ok, db_message = check_db_connection()
    
    return HealthResponse(
        success=True,
        status="healthy" if db_ok else "degraded",
        app=settings.APP_NAME,
        environment=settings.APP_ENV,
        database={
            "connected": db_ok,
            "message": db_message
        },
        message="System fully operational" if db_ok else "System operational in degraded mode (database offline)"
    )
