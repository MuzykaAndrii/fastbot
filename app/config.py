from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import EmailStr, computed_field, AnyUrl


BASE_DIR = Path(__file__).resolve().parent.parent
BOT_PREFIX = "bot"
TEMPLATES_DIR = BASE_DIR / "app/backend/pages/templates"
AUTH_TOKEN_NAME = "auth_token"

ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # MODE: Literal["DEV", "TEST", "PROD"]
    DEBUG: bool
    BOT_TOKEN: str

    HOST_URL: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    API_KEY: str

    BASE_ADMIN_EMAIL: EmailStr
    BASE_ADMIN_PASS: str

    SENTRY_DSN: AnyUrl


    @computed_field # type: ignore[misc]
    @property
    def WEBHOOK_PATH(self) -> str:
        return f"/{BOT_PREFIX}{self.BOT_TOKEN}"
    
    @computed_field  # type: ignore[misc]
    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.HOST_URL}{self.WEBHOOK_PATH}"


settings = Settings()  # type: ignore[call-arg]