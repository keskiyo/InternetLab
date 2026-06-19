"""Logging setup: rotating app log + dedicated email log + console."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler

from app.core.paths import APP_LOG_PATH, EMAIL_LOG_PATH, ensure_dirs

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

APP_LOGGER_NAME = "app"
EMAIL_LOGGER_NAME = "app.email"

_configured = False


def _rotating_handler(path: str, level: int) -> RotatingFileHandler:
    handler = RotatingFileHandler(
        path, maxBytes=2_000_000, backupCount=5, encoding="utf-8-sig"
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    return handler


def setup_logging() -> None:
    """Configure root and email loggers. Idempotent."""
    global _configured
    if _configured:
        return
    ensure_dirs()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))

    app_logger = logging.getLogger(APP_LOGGER_NAME)
    app_logger.setLevel(logging.INFO)
    app_logger.handlers.clear()
    app_logger.addHandler(_rotating_handler(str(APP_LOG_PATH), logging.INFO))
    app_logger.addHandler(console)
    app_logger.propagate = False

    # Dedicated email logger -> logs/emails.log + console
    email_logger = logging.getLogger(EMAIL_LOGGER_NAME)
    email_logger.setLevel(logging.INFO)
    email_logger.handlers.clear()
    email_logger.addHandler(_rotating_handler(str(EMAIL_LOG_PATH), logging.INFO))
    email_logger.addHandler(console)
    email_logger.propagate = False

    _configured = True


def get_logger(name: str = APP_LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(name)
