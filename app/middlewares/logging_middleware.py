import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        inicio = time.perf_counter()

        # Generar Correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        logger.info(
            "[CID=%s] --> %s %s",
            correlation_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)

        except Exception:
            duracion = (time.perf_counter() - inicio) * 1000

            logger.exception(
                "[CID=%s] ERROR %s %s (%.2f ms)",
                correlation_id,
                request.method,
                request.url.path,
                duracion,
            )
            raise

        duracion = (time.perf_counter() - inicio) * 1000

        logger.info(
            "[CID=%s] <-- %s %s %s (%.2f ms)",
            correlation_id,
            request.method,
            request.url.path,
            response.status_code,
            duracion,
        )

        # Devolver el Correlation ID al cliente
        response.headers["X-Correlation-ID"] = correlation_id

        return response
