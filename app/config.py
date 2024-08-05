from pathlib import Path
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import EmailStr, computed_field


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "app/backend/pages/templates"

ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    MODE: Literal["DEV", "TEST", "PROD"]
    DEBUG: bool
    BOT_TOKEN: str

    HOST_URL: str

    API_KEY: str

    BASE_ADMIN_EMAIL: EmailStr
    BASE_ADMIN_PASS: str


    @computed_field # type: ignore[misc]
    @property
    def WEBHOOK_PATH(self) -> str:
        return f"/bot{self.BOT_TOKEN}"
    
    @computed_field  # type: ignore[misc]
    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.HOST_URL}{self.WEBHOOK_PATH}"


settings = Settings()  # type: ignore[call-arg]