from sqlalchemy import select

from .session import async_session_maker


async def ping_db() -> None:
    async with async_session_maker() as session:
        await session.execute(select(1))