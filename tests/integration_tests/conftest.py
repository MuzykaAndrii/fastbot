import pytest


from app.backend.components.db import database
from app.backend.components import UnitOfWork



@pytest.fixture(scope="session")
async def uow() -> UnitOfWork:
    return UnitOfWork(database.session_maker)