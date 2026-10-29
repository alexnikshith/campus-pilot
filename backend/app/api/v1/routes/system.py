from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import ResponseEnvelope, PaginationParams, PaginatedResponse
from app.core.exceptions import (
    EntityNotFoundException,
    ConflictException,
    BadRequestException,
    ValidationException
)

router = APIRouter(prefix="/system", tags=["System Foundation"])

class EchoPayload(BaseModel):
    message: str = Field(min_length=3, max_length=100, description="Message to echo back")
    category: Optional[str] = Field(default="general", description="Message category")

@router.get("/echo", response_model=ResponseEnvelope[EchoPayload])
def echo_message(msg: str = Query(..., min_length=3)) -> ResponseEnvelope[EchoPayload]:
    """Echo endpoint verifying ResponseEnvelope wrapping and query validation."""
    return ResponseEnvelope(
        success=True,
        data=EchoPayload(message=msg, category="echo"),
        message="Message echoed successfully"
    )

@router.post("/validate", response_model=ResponseEnvelope[EchoPayload], status_code=status.HTTP_201_CREATED)
def validate_payload(payload: EchoPayload) -> ResponseEnvelope[EchoPayload]:
    """POST endpoint demonstrating Pydantic payload validation and ResponseEnvelope output."""
    return ResponseEnvelope(
        success=True,
        data=payload,
        message="Payload validated successfully"
    )

@router.get("/trigger-error/{error_type}")
def trigger_error_test(error_type: str):
    """
    Test endpoint for verifying that centralized exception handlers catch domain exceptions
    and return normalized ErrorEnvelope responses.
    """
    if error_type == "not-found":
        raise EntityNotFoundException(entity_name="DemonstrationEntity", identifier="demo-999")
    elif error_type == "conflict":
        raise ConflictException(message="A resource with the specified identifier already exists.")
    elif error_type == "bad-request":
        raise BadRequestException(message="The supplied request parameters cannot be processed.")
    elif error_type == "validation":
        raise ValidationException(
            message="Domain validation failed.",
            details=[{"field": "score", "issue": "Score cannot be negative"}]
        )
    return ResponseEnvelope(success=True, message=f"No error triggered for type '{error_type}'")

@router.get("/paginate-demo", response_model=ResponseEnvelope[PaginatedResponse[str]])
def demo_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50)
) -> ResponseEnvelope[PaginatedResponse[str]]:
    """Demonstrates PaginatedResponse construction with metadata navigation flags."""
    sample_pool = [f"Item-{i}" for i in range(1, 23)]  # 22 items
    params = PaginationParams(page=page, page_size=page_size)
    
    start = params.offset
    end = start + params.page_size
    sliced = sample_pool[start:end]

    paginated = PaginatedResponse.create(
        items=sliced,
        total=len(sample_pool),
        page=params.page,
        page_size=params.page_size
    )

    return ResponseEnvelope(
        success=True,
        data=paginated,
        message="Paginated list retrieved successfully"
    )

