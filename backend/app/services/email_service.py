"""Email service using the Strategy pattern.

EmailSenderInterface  - abstract strategy
MockEmailSender       - logs nicely to console + logs/emails.log (dev/test)
SMTPEmailSender       - real SMTP implementation (production stub)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.core.config import settings
from app.core.logging import EMAIL_LOGGER_NAME, get_logger
from app.schemas.contact import AIAnalysis, ContactCreate

email_logger = get_logger(EMAIL_LOGGER_NAME)
logger = get_logger()


class EmailSenderInterface(ABC):
    """Abstract email strategy."""

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: ...


class MockEmailSender(EmailSenderInterface):
    """Pretty-logs 'sent' emails instead of delivering them."""

    def send(self, to: str, subject: str, body: str) -> None:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        rendered = (
            "\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║  📧  MOCK EMAIL                                               ║\n"
            "╠══════════════════════════════════════════════════════════════╣\n"
            f"║  Time:    {ts}\n"
            f"║  To:      {to}\n"
            f"║  Subject: {subject}\n"
            "╟──────────────────────────────────────────────────────────────╢\n"
            f"{body}\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        email_logger.info(rendered)


class SMTPEmailSender(EmailSenderInterface):
    """Real SMTP sender (stub). Wire up smtplib/aiosmtplib for production."""

    def __init__(self, host: str = "", port: int = 587) -> None:
        self._host = host
        self._port = port

    def send(self, to: str, subject: str, body: str) -> None:  # pragma: no cover
        raise NotImplementedError(
            "SMTPEmailSender is not configured. Set EMAIL_MOCK_MODE=true "
            "or implement SMTP delivery here."
        )


def get_email_sender() -> EmailSenderInterface:
    """Factory selecting the strategy based on settings."""
    if settings.email_mock_mode:
        return MockEmailSender()
    return SMTPEmailSender()


class EmailService:
    """High-level notifications built on top of a sender strategy."""

    def __init__(self, sender: EmailSenderInterface | None = None) -> None:
        self._sender = sender or get_email_sender()

    def send_owner_notification(self, payload: ContactCreate, ai: AIAnalysis) -> None:
        body = (
            f"║  Новая заявка с лендинга:\n"
            f"║   • Имя:        {payload.name}\n"
            f"║   • Телефон:    {payload.phone}\n"
            f"║   • Email:      {payload.email}\n"
            f"║   • Комментарий: {payload.comment}\n"
            f"║  ── AI анализ ({ai.status}) ──\n"
            f"║   • Тональность: {ai.sentiment}\n"
            f"║   • Категория:   {ai.category}\n"
            f"║   • Черновик:    {ai.draft_reply}"
        )
        self._safe_send(settings.owner_email, "Новая заявка с лендинга", body)

    def send_user_confirmation(self, payload: ContactCreate, ai: AIAnalysis) -> None:
        body = (
            f"║  Здравствуйте, {payload.name}!\n"
            f"║  Спасибо за заявку — я свяжусь с вами в ближайшее время.\n"
            f"║  ── Предварительный ответ ──\n"
            f"║  {ai.draft_reply}"
        )
        self._safe_send(str(payload.email), "Ваша заявка принята", body)

    def _safe_send(self, to: str, subject: str, body: str) -> None:
        try:
            self._sender.send(to, subject, body)
        except Exception:
            # Email must never break the request flow.
            logger.exception("email: failed to send to %s", to)
