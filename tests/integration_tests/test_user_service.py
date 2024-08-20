from typing import Any

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.models import User
from app.backend.users.services import UserService
from app.backend.components.config import app_settings


@pytest.mark.usefixtures("clean_db")
class TestUserService:
    async def test_get_or_create_by_id(self, user_service: UserService, mock_user: dict[str, Any]):
        # Act
        user = await user_service.get_or_create_by_id(mock_user["id"])
        
        # Assert
        assert user is not None
        assert user.id == mock_user["id"]


    async def test_get_by_id(self, user_service: UserService, db_mock_user: User):
        # Act
        user = await user_service.get_by_id(db_mock_user.id)
        
        # Assert
        assert user is not None
        assert user.id == db_mock_user.id
        assert user.email == db_mock_user.email


    async def test_get_by_email(self, user_service: UserService, db_mock_user: User):
        # Act
        user = await user_service.get_by_email(db_mock_user.email)
        
        # Assert
        assert user is not None
        assert user.id == db_mock_user.id
        assert user.email == db_mock_user.email


    async def test_ensure_admin_exists_creates_admin_if_none_exists(self, session: AsyncSession, user_service: UserService):
        # Act
        await user_service.ensure_admin_exists()
        
        # Assert
        admin_users = await session.scalars(select(User).filter_by(is_superuser=True))
        admin_users = list(admin_users)
        assert len(admin_users) == 1
        assert admin_users[0].email == app_settings.BASE_ADMIN_EMAIL


    async def test_ensure_admin_exists_does_not_create_if_admin_exists(self, session: AsyncSession, user_service: UserService):
        # Arrange
        base_admin_user = {
            "email": app_settings.BASE_ADMIN_EMAIL,
            "password_hash": b"somehash",
            "is_superuser": True,
        }
        stmt = insert(User).values(**base_admin_user)
        await session.execute(stmt)
        await session.commit()

        # Act
        await user_service.ensure_admin_exists()
        
        # Assert
        admin_users = await session.scalars(select(User).filter_by(is_superuser=True))
        admin_users = list(admin_users)
        assert len(admin_users) == 1  # Ensure only one admin created