from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


_DB_URL_PATTERN="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int

    DB_NAME: str = Field(validation_alias="POSTGRES_DB")
    DB_USER: str = Field(validation_alias="POSTGRES_USER")
    DB_PASS: str = Field(validation_alias="POSTGRES_PASSWORD")

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        return _DB_URL_PATTERN.format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )
