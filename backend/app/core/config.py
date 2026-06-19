"""Application configuration loaded from environment / .env."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.paths import BASE_DIR


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    # Yandex GPT
    yandex_folder_id: str
    yandex_api_key: str
    yandex_gpt_model_uri: str = "yandexgpt"

    # App
    app_env: str = "development"
    rate_limit_max_requests: int = 3
    rate_limit_window_minutes: int = 60

    # Email
    email_mock_mode: bool = True
    owner_email: str = "owner@example.com"

    # CORS — comma-separated list of allowed origins
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Yandex GPT endpoint + timeout
    yandex_gpt_url: str = (
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    )
    ai_timeout_seconds: float = 10.0

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def model_uri(self) -> str:
        return f"gpt://{self.yandex_folder_id}/{self.yandex_gpt_model_uri}"


settings = Settings()
