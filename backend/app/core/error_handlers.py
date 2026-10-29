import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException
from app.schemas.common import ErrorEnvelope, ErrorDetail

logger = logging.getLogger("placementpilot.errors")

def register_error_handlers(app: FastAPI) -> None:
    """
    Registers comprehensive centralized exception handlers on the FastAPI application instance.
    Ensures all error responses adhere to the standard ErrorEnvelope format without leaking secrets.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(
            f"AppException: code={exc.code} status={exc.status_code} "
            f"path={request.url.path} message='{exc.message}'"
        )
        envelope = ErrorEnvelope(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                details=exc.details
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        # Format Pydantic field-level errors for clean frontend display
        formatted_errors = []
        for err in exc.errors():
            loc = " -> ".join(str(item) for item in err.get("loc", []))
            formatted_errors.append({
                "field": loc,
                "message": err.get("msg", "Validation error"),
                "type": err.get("type", "value_error")
            })

        logger.info(f"Validation error on {request.method} {request.url.path}: {len(formatted_errors)} issues")
        envelope = ErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Request validation failed. Please review the provided fields.",
                details=formatted_errors
            )
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=envelope.model_dump()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.info(f"HTTPException: status={exc.status_code} path={request.url.path} detail='{exc.detail}'")
        code = "HTTP_ERROR"
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            code = "ROUTE_NOT_FOUND"
        elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            code = "METHOD_NOT_ALLOWED"
        elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
            code = "UNAUTHORIZED"
        elif exc.status_code == status.HTTP_403_FORBIDDEN:
            code = "FORBIDDEN"

        envelope = ErrorEnvelope(
            error=ErrorDetail(
                code=code,
                message=str(exc.detail),
                details=None
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope.model_dump()
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        # Log the full database error server-side for diagnostics, but never expose it to client
        error_class = type(exc).__name__
        logger.error(f"Database error on {request.method} {request.url.path} [{error_class}]: {exc}", exc_info=True)

        envelope = ErrorEnvelope(
            error=ErrorDetail(
                code="DATABASE_ERROR",
                message="An internal database error occurred. The operation could not be completed.",
                details={"error_type": error_class}
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=envelope.model_dump()
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.critical(f"Unhandled server exception on {request.method} {request.url.path}: {exc}", exc_info=True)
        envelope = ErrorEnvelope(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred. Our engineering team has been notified.",
                details=None
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=envelope.model_dump()
        )

