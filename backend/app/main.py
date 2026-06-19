"""FastAPI entry point: app wiring, CORS, middleware, error handlers, startup."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import contact, health, metrics
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.paths import ensure_dirs
from app.db.session import init_db

setup_logging()
logger = get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    ensure_dirs()
    await init_db()
    logger.info("Application started (env=%s)", settings.app_env)
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="Developer Landing API",
    description="Backend service for a developer landing page with YandexGPT AI.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(contact.router)
app.include_router(metrics.router)
