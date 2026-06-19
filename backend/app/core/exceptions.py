"""Domain exceptions and global exception handlers."""
from __future__ import annotations

import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger()


class AppError(Exception):
    """Base application error carrying an HTTP status + client-safe message."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class RateLimitExceeded(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Too many requests. Please try again later."


def register_exception_handlers(app: FastAPI) -> None:
    """Attach handlers returning clean JSON {"detail": "..."}."""

    @app.exception_handler(AppError)
    async def _app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        logger.warning("AppError: %s", exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Surface the first readable validation message.
        errors = exc.errors()
        msg = "Validation error"
        if errors:
            loc = ".".join(str(p) for p in errors[0].get("loc", []) if p != "body")
            msg = f"{loc}: {errors[0].get('msg', msg)}" if loc else errors[0].get("msg", msg)
        return JSONResponse(status_code=422, content={"detail": msg})

    @app.exception_handler(StarletteHTTPException)
    async def _http_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": str(exc.detail)}
        )

    @app.exception_handler(Exception)
    async def _unhandled_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception:\n%s", traceback.format_exc())
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
