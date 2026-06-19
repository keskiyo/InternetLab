"""CRUD access for ContactRequest."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactRequest
from app.schemas.contact import AIAnalysis, ContactCreate


class ContactRepository:
    """Data-access layer for contact requests."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, payload: ContactCreate, ai: AIAnalysis) -> ContactRequest:
        entity = ContactRequest(
            name=payload.name,
            phone=payload.phone,
            email=str(payload.email),
            comment=payload.comment,
            sentiment=ai.sentiment,
            category=ai.category,
            draft_reply=ai.draft_reply,
            ai_status=ai.status,
        )
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def count_total(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(ContactRequest)
        )
        return int(result.scalar_one())

    async def count_by_ai_status(self, status: str) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(ContactRequest)
            .where(ContactRequest.ai_status == status)
        )
        return int(result.scalar_one())
