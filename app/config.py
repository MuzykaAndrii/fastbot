from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import EmailStr, computed_field, AnyUrl


BASE_DIR = Path(__file__).resolve().parent.parent
BOT_PREFIX = "bot"
DB_URL_PATTERN="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
TEMPLATES_DIR = BASE_DIR / "app/backend/pages/templates"
AUTH_TOKEN_NAME = "auth_token"

ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEBUG: bool
    BOT_TOKEN: str

    HOST_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    API_KEY: str
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int

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
    
    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        return DB_URL_PATTERN.format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

settings = Settings()  # type: ignore[call-arg]