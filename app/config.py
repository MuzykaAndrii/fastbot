from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import computed_field


BASE_DIR = Path(__file__).resolve().parent.parent
BOT_PREFIX = "bot"

env_file_path = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding="utf-8")

    DEBUG: bool
    BOT_TOKEN: str

    HOST_URL: str

    @computed_field
    @property
    def WEBHOOK_PATH(self) -> str:
        return f"/{BOT_PREFIX}{self.BOT_TOKEN}"
    
    @computed_field
    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.HOST_URL}{self.WEBHOOK_PATH}"

settings = Settings()