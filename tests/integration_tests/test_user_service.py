from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.models import User
from app.backend.users.services import UserService


async def test_get_or_create_by_id(user_service: UserService, mock_user: dict[str, Any], clean_db):
    # Act
    user = await user_service.get_or_create_by_id(mock_user["id"])
    
    # Assert
    assert user is not None
    assert user.id == mock_user["id"]


async def test_get_by_id(user_service: UserService, db_mock_user: User, clean_db):
    # Act
    user = await user_service.get_by_id(db_mock_user.id)
    
    # Assert
    assert user is not None
    assert user.id == db_mock_user.id
    assert user.email == db_mock_user.email


async def test_get_by_email(user_service: UserService, db_mock_user: User, clean_db):
    # Act
    user = await user_service.get_by_email(db_mock_user.email)
    
    # Assert
    assert user is not None
    assert user.id == db_mock_user.id
    assert user.email == db_mock_user.email