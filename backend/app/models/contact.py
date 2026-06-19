"""ORM model for contact requests."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ContactRequest(Base):
    """A submitted contact form request enriched with AI analysis."""

    __tablename__ = "contact_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)

    # AI analysis fields
    sentiment: Mapped[str] = mapped_column(
        String(20), nullable=False, default="neutral"
    )
    category: Mapped[str] = mapped_column(
        String(40), nullable=False, default="consulting"
    )
    draft_reply: Mapped[str] = mapped_column(Text, nullable=False, default="")
    ai_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="fallback"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
