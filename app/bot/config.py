from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import computed_field


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BOT_TOKEN: str
    HOST_URL: str

    @computed_field # type: ignore[misc]
    @property
    def WEBHOOK_PATH(self) -> str:
        return f"/bot{self.BOT_TOKEN}"
    
    @computed_field  # type: ignore[misc]
    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.HOST_URL}{self.WEBHOOK_PATH}"
