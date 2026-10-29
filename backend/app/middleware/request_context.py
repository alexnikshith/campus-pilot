import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("placementpilot.requests")

class RequestIDAndTimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    1. Attaches a unique X-Request-ID to every request & response for distributed tracing.
    2. Calculates request execution duration in milliseconds.
    3. Emits structured log telemetry for every request.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Retrieve incoming request ID if provided by client or reverse proxy, else generate UUID4
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        start_time = time.perf_counter()
        
        try:
            response = await call_next(request)
        except Exception:
            # Let registered exception handlers catch and format, but still measure duration
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                f"[{request_id}] {request.method} {request.url.path} - FAILED after {duration_ms:.2f}ms"
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000

        # Inject telemetry headers into the HTTP response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"

        # Structured log line
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> status={response.status_code} duration={duration_ms:.2f}ms"
        )

        return response

