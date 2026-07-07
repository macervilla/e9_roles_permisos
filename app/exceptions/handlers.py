from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = getattr(request.state, "correlation_id", "sin-correlation-id")

    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "mensaje": "Error interno del servidor",
            "correlation_id": correlation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
