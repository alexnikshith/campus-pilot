from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field
import math

T = TypeVar("T")

class ResponseEnvelope(BaseModel, Generic[T]):
    """Standardized API response wrapper for successful operations."""
    success: bool = Field(default=True, description="Indicates if the request succeeded")
    data: Optional[T] = Field(default=None, description="Payload data returned by endpoint")
    message: str = Field(default="Operation completed successfully", description="User-facing summary message")

    model_config = {
        "arbitrary_types_allowed": True
    }


class ErrorDetail(BaseModel):
    """Structured error descriptor."""
    code: str = Field(description="Machine-readable error classification code")
    message: str = Field(description="Human-readable error description")
    details: Optional[Any] = Field(default=None, description="Granular error details or validation field issues")


class ErrorEnvelope(BaseModel):
    """Standardized API error response format across all endpoints."""
    success: bool = Field(default=False, description="Always False for error responses")
    error: ErrorDetail = Field(description="Detailed error payload")


class PaginationParams(BaseModel):
    """Standardized query parameters for paginated queries."""
    page: int = Field(default=1, ge=1, description="Page number starting at 1")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (1 to 100)")
    sort_by: str = Field(default="id", description="Field name to sort by")
    order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order: asc or desc")

    @property
    def offset(self) -> int:
        """Calculate SQL LIMIT offset from page and page_size."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Standardized envelope for paginated collection responses."""
    items: List[T] = Field(default_factory=list, description="Array of entities on current page")
    total: int = Field(ge=0, description="Total matching items across all pages")
    page: int = Field(ge=1, description="Current page number")
    page_size: int = Field(ge=1, description="Number of items per page")
    total_pages: int = Field(ge=0, description="Total number of available pages")
    has_next: bool = Field(description="True if another page exists after this one")
    has_prev: bool = Field(description="True if a previous page exists before this one")

    model_config = {
        "arbitrary_types_allowed": True
    }

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse[T]":
        """Factory method to construct paginated response with accurate navigation flags."""
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1 and total_pages > 0
        )
