import pytest

from app.backend.components.config import app_settings
from app.backend.components.db import database
from app.config import AppModes
from app.backend.db.base import Base
from app.backend.users.models import User  # noqa
from app.backend.vocabulary.models import VocabularySet, LanguagePair  # noqa


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert app_settings.MODE == AppModes.TEST

    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

