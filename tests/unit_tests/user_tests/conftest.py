from typing import Any

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.dal import UserDAL
from app.backend.users.models import User


@pytest.fixture(scope="function")
async def user_dal(session: AsyncSession) -> UserDAL:
    return UserDAL(session)
