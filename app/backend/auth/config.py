from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    TOKEN_KEY: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int
    REFRESH_TOKEN_LIFETIME_MINUTES: int