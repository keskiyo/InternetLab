"""Central filesystem paths. All relative to the backend/ root."""

from __future__ import annotations

from pathlib import Path

# backend/app/core/paths.py -> backend/
BASE_DIR: Path = Path(__file__).resolve().parents[2]

DATA_DIR: Path = BASE_DIR / "data"
LOGS_DIR: Path = BASE_DIR / "logs"

DB_PATH: Path = DATA_DIR / "app.db"
RATE_LIMIT_PATH: Path = DATA_DIR / "rate_limits.json"

APP_LOG_PATH: Path = LOGS_DIR / "app.log"
EMAIL_LOG_PATH: Path = LOGS_DIR / "emails.log"


def ensure_dirs() -> None:
    """Create runtime directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
