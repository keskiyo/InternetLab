"""Orchestrates the contact submission flow."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.repositories.contact_repo import ContactRepository
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.ai_service import AIService
from app.services.email_service import EmailService
from app.services.rate_limit import RateLimitService

logger = get_logger()


class ContactService:
    """Rate-limit -> AI analyze -> persist -> notify."""

    def __init__(
        self,
        session: AsyncSession,
        ai_service: AIService | None = None,
        email_service: EmailService | None = None,
        rate_limiter: RateLimitService | None = None,
    ) -> None:
        self._repo = ContactRepository(session)
        self._ai = ai_service or AIService()
        self._email = email_service or EmailService()
        self._rate_limiter = rate_limiter or RateLimitService()

    async def submit(
        self,
        payload: ContactCreate,
        client_ip: str,
        enforce_rate_limit: bool = True,
    ) -> ContactResponse:
        # 1. Rate limit only real form submissions (raises -> 429).
        if enforce_rate_limit:
            self._rate_limiter.check(client_ip)

        # 2. AI analysis (never raises; returns fallback on error).
        ai = await self._ai.analyze(payload.comment)

        # 3. Persist enriched record.
        entity = await self._repo.create(payload, ai)
        logger.info(
            "contact: stored #%d from %s (ai=%s)", entity.id, payload.email, ai.status
        )

        # 4. Notifications (mock; failures are swallowed inside EmailService).
        self._email.send_owner_notification(payload, ai)
        self._email.send_user_confirmation(payload, ai)

        return ContactResponse(
            id=entity.id,
            name=entity.name,
            email=payload.email,
            created_at=entity.created_at,
            ai=ai,
        )
