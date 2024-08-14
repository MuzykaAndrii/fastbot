import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.dal import UserDAL


@pytest.fixture(scope="function")
async def user_dal(session: AsyncSession) -> UserDAL:
    return UserDAL(session)