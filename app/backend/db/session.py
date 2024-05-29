from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from .config import DbSettings


def get_session_maker(db_settings: DbSettings):
    engine = create_async_engine(db_settings.DATABASE_URL)
    return async_sessionmaker(engine, expire_on_commit=False)