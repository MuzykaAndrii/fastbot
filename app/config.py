from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import computed_field


BASE_DIR = Path(__file__).resolve().parent.parent

env_file_path = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding="utf-8")

    DEBUG: bool
    BOT_TOKEN: str

    NGROK_URL: str
    HOST_URL: str

    @computed_field
    @property
    def WEBHOOK_URL(self) -> str:
        if self.DEBUG:
            return self.NGROK_URL
        else:
            return self.HOST_URL


settings = Settings()