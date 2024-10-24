from typing import Callable

from sqlalchemy.pool import NullPool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from .config import DbSettings


class DataBase:
    def __init__(self, settings: DbSettings):
        if settings.MODE == "TEST":
            engine_kwargs = {"poolclass": NullPool}
        else:
            engine_kwargs = {}

        self._engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
    
    @property
    def session_maker(self) -> Callable[[], AsyncSession]:
        return self._session_maker
    
    async def ping(self):
        async with self.session_maker() as session:
            await session.execute(select(1))
    
    @property
    def engine(self) -> AsyncEngine:
        return self._engine
