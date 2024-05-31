from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from .config import DbSettings


class DataBase:
    def __init__(self, settings: DbSettings):
        self._engine = create_async_engine(settings.DATABASE_URL)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
    
    @property
    def session_maker(self) -> Callable[[], AsyncSession]:
        return self._session_maker
    
    async def ping(self):
        async with self.session_maker() as session:
            await session.execute(select(1))
    
    @property
    def engine(self):
        return self._engine
