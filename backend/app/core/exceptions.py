from typing import Optional, Any

class AppException(Exception):
    """Base application exception for PlacementPilot."""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class EntityNotFoundException(AppException):
    """Raised when a requested resource does not exist."""
    def __init__(self, entity_name: str, identifier: Any, details: Optional[Any] = None):
        message = f"{entity_name} with identifier '{identifier}' was not found."
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details=details
        )


class BadRequestException(AppException):
    """Raised when request payload or parameters are semantically invalid."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            status_code=400,
            details=details
        )


class UnauthorizedException(AppException):
    """Raised when authentication credentials are missing, expired, or invalid."""
    def __init__(self, message: str = "Authentication credentials required or invalid", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
            details=details
        )


class ForbiddenException(AppException):
    """Raised when authenticated user lacks permission for the requested action."""
    def __init__(self, message: str = "Access denied for this resource", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
            details=details
        )


class ConflictException(AppException):
    """Raised when attempting to create duplicate entities (e.g., unique constraint)."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="RESOURCE_CONFLICT",
            status_code=409,
            details=details
        )


class ValidationException(AppException):
    """Raised when domain validation fails."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class RateLimitException(AppException):
    """Raised when request volume exceeds configured rate limits."""
    def __init__(self, message: str = "Too many requests. Please try again later.", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details
        )


class DatabaseException(AppException):
    """
    Raised when an unrecoverable database error occurs.
    Sanitizes database specifics to prevent leaking credentials or connection strings.
    """
    def __init__(self, message: str = "A database operation failed unexpectedly.", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details
        )

