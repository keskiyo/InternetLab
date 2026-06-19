"""File-based sliding-window rate limiter (per IP)."""

from __future__ import annotations

import json
import threading
import time

from app.core.config import settings
from app.core.exceptions import RateLimitExceeded
from app.core.logging import get_logger
from app.core.paths import RATE_LIMIT_PATH, ensure_dirs

logger = get_logger()

# A process-wide lock guards read-modify-write of the JSON file.
_lock = threading.Lock()


class RateLimitService:
    """Stores hit timestamps per IP in a JSON file."""

    def __init__(
        self,
        max_requests: int | None = None,
        window_minutes: int | None = None,
    ) -> None:
        self._max = max_requests or settings.rate_limit_max_requests
        self._window = (window_minutes or settings.rate_limit_window_minutes) * 60

    def _load(self) -> dict[str, list[float]]:
        if not RATE_LIMIT_PATH.exists():
            return {}
        try:
            with RATE_LIMIT_PATH.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return {k: list(v) for k, v in data.items()}
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("rate_limit: failed to read store (%s); resetting", exc)
        return {}

    def _save(self, store: dict[str, list[float]]) -> None:
        ensure_dirs()
        tmp = RATE_LIMIT_PATH.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(store, fh)
        tmp.replace(RATE_LIMIT_PATH)

    def check(self, ip: str) -> None:
        """Register a hit for `ip`. Raise RateLimitExceeded when over limit."""
        now = time.time()
        cutoff = now - self._window
        with _lock:
            store = self._load()
            hits = [t for t in store.get(ip, []) if t > cutoff]
            if len(hits) >= self._max:
                logger.warning("rate_limit: IP %s exceeded (%d hits)", ip, len(hits))
                raise RateLimitExceeded(
                    f"Превышен лимит: не более {self._max} заявок "
                    f"за {self._window // 60} мин."
                )
            hits.append(now)
            store[ip] = hits
            # Drop empty/expired buckets to keep the file small.
            store = {k: v for k, v in store.items() if v}
            self._save(store)
