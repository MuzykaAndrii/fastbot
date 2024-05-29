from pydantic import AnyUrl, Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class SentrySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    dsn: AnyUrl = Field(validation_alias="sentry_dsn")