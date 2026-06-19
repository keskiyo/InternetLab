"""Contact submission endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.middleware import get_client_ip
from app.db.session import get_session
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import ContactService

router = APIRouter(prefix="/api", tags=["contact"])

# Frontend form sends this header so we can rate-limit only genuine submissions
WEB_FORM_HEADER = "x-contact-source"
WEB_FORM_VALUE = "web-form"


@router.post("/contact", response_model=ContactResponse)
async def create_contact(
    payload: ContactCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ContactResponse:
    from_web_form = request.headers.get(WEB_FORM_HEADER) == WEB_FORM_VALUE
    service = ContactService(session)
    return await service.submit(
        payload, get_client_ip(request), enforce_rate_limit=from_web_form
    )
