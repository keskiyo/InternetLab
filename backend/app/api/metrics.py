"""Metrics endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.contact_repo import ContactRepository
from app.schemas.contact import MetricsResponse

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
async def metrics(
    session: AsyncSession = Depends(get_session),
) -> MetricsResponse:
    repo = ContactRepository(session)
    return MetricsResponse(
        total_requests=await repo.count_total(),
        ai_success=await repo.count_by_ai_status("success"),
        ai_fallback=await repo.count_by_ai_status("fallback"),
    )
