import pytest

from app.backend.components.config import app_settings
from app.backend.components.db import database
from app.config import AppModes
from app.backend.db.base import Base
from app.backend.users.models import User  # noqa
from app.backend.vocabulary.models import VocabularySet, LanguagePair  # noqa
from tests.mocks import get_mock_users_data


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert app_settings.MODE == AppModes.TEST

    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope="function")
async def session():
    async with database.session_maker() as session:
        yield session


@pytest.fixture
async def mock_users_data():
    return get_mock_users_data()