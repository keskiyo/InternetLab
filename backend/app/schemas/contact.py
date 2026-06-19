"""Pydantic request/response schemas."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

Sentiment = Literal["positive", "negative", "neutral"]
Category = Literal["frontend", "backend", "design", "consulting"]
AIStatus = Literal["success", "fallback"]

_PHONE_RE = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


class ContactCreate(BaseModel):
    """Incoming contact form payload."""

    name: str = Field(..., min_length=2, max_length=120)
    phone: str = Field(..., min_length=7, max_length=40)
    email: EmailStr
    comment: str = Field(..., min_length=5, max_length=2000)

    @field_validator("name", "comment")
    @classmethod
    def _strip_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty")
        return v

    @field_validator("phone")
    @classmethod
    def _valid_phone(cls, v: str) -> str:
        v = v.strip()
        if not _PHONE_RE.match(v):
            raise ValueError("invalid phone number")
        return v


class AIAnalysis(BaseModel):
    """Structured result from the AI service."""

    sentiment: Sentiment = "neutral"
    category: Category = "consulting"
    draft_reply: str = ""
    status: AIStatus = "fallback"


class ContactResponse(BaseModel):
    """Response returned after a successful submission."""

    id: int
    name: str
    email: EmailStr
    created_at: datetime
    ai: AIAnalysis
    message: str = "Заявка принята. Спасибо!"


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    env: str


class MetricsResponse(BaseModel):
    total_requests: int
    ai_success: int
    ai_fallback: int
