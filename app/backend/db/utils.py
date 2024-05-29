from sqlalchemy import select

from app.backend.components.db import async_session_maker


async def ping_db() -> None:
    async with async_session_maker() as session:
        await session.execute(select(1))