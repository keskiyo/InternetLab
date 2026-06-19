"""YandexGPT integration with graceful fallback.

Never raises: any error / timeout returns a default AIAnalysis(status="fallback").
"""

from __future__ import annotations

import asyncio
import json
import re
import sys

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.contact import AIAnalysis

logger = get_logger()

_SYSTEM_PROMPT = (
    "Ты ассистент разработчика. Проанализируй текст заявки и верни СТРОГО JSON "
    'без markdown: {"sentiment": "positive/negative/neutral", '
    '"category": "frontend/backend/design/consulting", '
    '"draft_reply": "текст ответа"}'
)

_DEFAULT_REPLY = (
    "Спасибо за обращение! Я получил вашу заявку и свяжусь с вами "
    "в ближайшее время, чтобы обсудить детали."
)

_VALID_SENTIMENTS = {"positive", "negative", "neutral"}
_VALID_CATEGORIES = {"frontend", "backend", "design", "consulting"}

# YandexGPT often answers in Russian despite the prompt — normalize synonyms
# so we don't silently fall back to defaults on a successful call.
_SENTIMENT_SYNONYMS = {
    "положительный": "positive",
    "позитивный": "positive",
    "позитив": "positive",
    "отрицательный": "negative",
    "негативный": "negative",
    "негатив": "negative",
    "нейтральный": "neutral",
    "нейтрально": "neutral",
}
_CATEGORY_KEYWORDS = {
    "frontend": ("frontend", "фронт", "верст", "ui", "интерфейс"),
    "backend": ("backend", "бэк", "бек", "сервер", "api", "база"),
    "design": ("design", "дизайн", "ux", "ui/ux", "макет"),
    "consulting": ("consult", "консульт", "совет", "запрос"),
}

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def _normalize_sentiment(raw: str) -> str:
    if raw in _VALID_SENTIMENTS:
        return raw
    return _SENTIMENT_SYNONYMS.get(raw, "neutral")


def _normalize_category(raw: str) -> str:
    if raw in _VALID_CATEGORIES:
        return raw
    for category, keywords in _CATEGORY_KEYWORDS.items():
        if any(kw in raw for kw in keywords):
            return category
    return "consulting"


def _fallback(reason: str) -> AIAnalysis:
    logger.warning("ai_service: fallback used (%s)", reason)
    return AIAnalysis(
        sentiment="neutral",
        category="consulting",
        draft_reply=_DEFAULT_REPLY,
        status="fallback",
    )


def _extract_json(text: str) -> dict[str, str]:
    """Extract a JSON object from a model reply that may wrap it in fences."""
    fenced = _JSON_FENCE_RE.search(text)
    candidate = fenced.group(1) if fenced else text
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = candidate[start : end + 1]
    return json.loads(candidate)


def _coerce(parsed: dict[str, str]) -> AIAnalysis:
    sentiment = str(parsed.get("sentiment", "neutral")).lower().strip()
    category = str(parsed.get("category", "consulting")).lower().strip()
    draft = str(parsed.get("draft_reply", "")).strip() or _DEFAULT_REPLY
    return AIAnalysis(
        sentiment=_normalize_sentiment(sentiment),
        category=_normalize_category(category),
        draft_reply=draft,
        status="success",
    )


def _build_transport() -> httpx.AsyncHTTPTransport | None:
    """On Windows, async httpcore may pick an unreachable IPv6 address with no
    Happy-Eyeballs fallback. Binding the source to 0.0.0.0 forces IPv4."""
    if sys.platform == "win32":
        return httpx.AsyncHTTPTransport(local_address="0.0.0.0")
    return None


class AIService:
    """Calls YandexGPT Foundation Models completion API."""

    async def analyze(self, comment: str) -> AIAnalysis:
        try:
            return await asyncio.wait_for(
                self._request(comment), timeout=settings.ai_timeout_seconds
            )
        except asyncio.TimeoutError:
            return _fallback("timeout")
        except Exception as exc:  # noqa: BLE001 - service must not crash
            return _fallback(f"{type(exc).__name__}: {exc}")

    async def _request(self, comment: str) -> AIAnalysis:
        headers = {
            "Authorization": f"Api-Key {settings.yandex_api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "modelUri": settings.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 1000,
            },
            "messages": [
                {"role": "system", "text": _SYSTEM_PROMPT},
                {"role": "user", "text": comment},
            ],
        }
        async with httpx.AsyncClient(
            timeout=settings.ai_timeout_seconds, transport=_build_transport()
        ) as client:
            resp = await client.post(
                settings.yandex_gpt_url, headers=headers, json=body
            )
            resp.raise_for_status()
            data = resp.json()

        text = (
            data.get("result", {})
            .get("alternatives", [{}])[0]
            .get("message", {})
            .get("text", "")
        )
        if not text:
            return _fallback("empty response")
        try:
            return _coerce(_extract_json(text))
        except (json.JSONDecodeError, ValueError, KeyError) as exc:
            return _fallback(f"parse error: {exc}")
