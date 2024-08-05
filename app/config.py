from enum import Enum
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import EmailStr


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "app/backend/pages/templates"


class AppModes(str, Enum):
    DEV = "DEV"
    TEST = "TEST"
    PROD = "PROD"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    MODE: AppModes
    DEBUG: bool

    BASE_ADMIN_EMAIL: EmailStr
    BASE_ADMIN_PASS: str
