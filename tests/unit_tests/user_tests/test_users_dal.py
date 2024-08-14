from typing import Any

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound, InvalidRequestError, StatementError

from app.backend.users.dal import UserDAL
from app.backend.users.models import User


async def test_create_user(user_dal: UserDAL, mock_user: dict[str, Any]):
    """Test creating a new user."""
    user = await user_dal.create(**mock_user)

    assert user.id is not None
    assert user.username == mock_user["username"]
    assert user.email == mock_user["email"]
    assert user.password_hash == mock_user["password_hash"]
    assert user.is_superuser == mock_user["is_superuser"]


async def test_create_user_duplicate_email(user_dal: UserDAL, session: AsyncSession):
    """Test creating a user with a duplicate email raises an exception."""
    mock_user = {"username": "user1", "email": "duplicate@example.com", "password_hash": b"pwd1"}
    stmt = insert(User).values(**mock_user).returning(User)
    await session.execute(stmt)

    with pytest.raises(IntegrityError):
        await user_dal.create(**mock_user)


async def test_create_user_with_wrong_field_name(user_dal: UserDAL):
    """Test creating a user with a field name that doesn't exist."""
    invalid_user_data = {
        "username": "invalid_user",
        "email": "invalid_user@example.com",
        "password_hash": b"somehashedpassword",
        "non_existent_field": "some_value",  # Incorrect field name
    }

    with pytest.raises(TypeError):
        await user_dal.create(**invalid_user_data)


@pytest.mark.parametrize(
    "user_data",
    [{
        "username": 123,  # Invalid type
        "email": "valid_user@example.com",
        "password_hash": b"validpassword",
        "is_superuser": False,
    },
    {
        "username": "valid_user",
        "email": 123,  # Invalid type
        "password_hash": b"validpassword",
        "is_superuser": False,
    },
    {
        "username": "valid_user",
        "email": "valid_user@example.com",
        "password_hash": "string_instead_of_bytes",  # Invalid type
        "is_superuser": False,
    },
    {
        "username": "valid_user",
        "email": "valid_user@example.com",
        "password_hash": b"validpassword",
        "is_superuser": "not_a_boolean",  # Invalid type
    }]
)
async def test_create_user_with_wrong_field_type(user_dal: UserDAL, user_data: dict):
    """Test creating a user with incorrect field types."""
    
    with pytest.raises(StatementError):
        await user_dal.create(**user_data)


async def test_get_user_by_id(user_dal: UserDAL, session: AsyncSession, mock_user: dict[str, Any]):
    stmt = insert(User).values(**mock_user).returning(User)
    result = await session.execute(stmt)
    user = result.scalar_one()

    fetched_user = await user_dal.get_by_id(user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.username == mock_user["username"]
    assert fetched_user.email == mock_user["email"]
    assert fetched_user.password_hash == mock_user["password_hash"]


async def test_get_user_by_non_existent_id(user_dal: UserDAL):
    """Test getting a user by a non-existent ID returns None."""
    non_existent_id = 99999
    user = await user_dal.get_by_id(non_existent_id)

    assert user is None


async def test_get_all_users(user_dal: UserDAL, session: AsyncSession, create_mock_users, mock_users_list: list[dict[str, Any]]):
    db_users = await user_dal.get_all()

    assert len(db_users) == len(mock_users_list)

    for mock_user, db_user in zip(db_users, mock_users_list):
        assert db_user.username == mock_user["username"]
        assert db_user.email == mock_user["email"]
        assert db_user.password_hash == mock_user["password_hash"]
        assert db_user.is_superuser == mock_user["is_superuser"]


async def test_delete_user_by_id(user_dal: UserDAL, session: AsyncSession, mock_user: dict[str, Any]):
    stmt = insert(User).values(**mock_user).returning(User)
    result = await session.execute(stmt)
    user = result.scalar_one()

    deleted_user = await user_dal.delete_by_id(user.id)

    assert deleted_user.id == user.id

    stmt = select(User).where(User.id == user.id)
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is None


async def test_delete_user_by_non_existent_id(user_dal: UserDAL):
    """Test deleting a user by a non-existent ID raises an exception."""
    non_existent_id = 99999

    with pytest.raises(NoResultFound):
        await user_dal.delete_by_id(non_existent_id)


async def test_filter_users_by_criteria(user_dal: UserDAL, session: AsyncSession, create_mock_users, mock_users_list: list[dict[str, Any]]):
    """Test filtering users by criteria."""

    found = await user_dal.filter_by(**mock_users_list[1])  # filter random user
    assert len(found) == 1


async def test_filter_users_by_no_match(user_dal: UserDAL):
    """Test filtering users by criteria with no matches returns an empty list."""
    non_existent_criteria = {"username": "nonexistent", "email": "nonexistent@example.com"}
    users = await user_dal.filter_by(**non_existent_criteria)

    assert len(users) == 0


async def test_filter_users_by_wrong_filed(user_dal: UserDAL):
    user_with_wrong_field = {"username": "someusername", "email": "someemail@example.com", "wrong_field": "some_data"}

    with pytest.raises(InvalidRequestError):
        await user_dal.filter_by(**user_with_wrong_field)


async def test_get_admin_users(user_dal: UserDAL, session: AsyncSession, create_mock_users):
    """Test getting all admin users."""
    stmt = select(User).where(User.is_superuser == True)
    result = await session.execute(stmt)
    admins = result.scalars().all()

    admins = await user_dal.get_admin_users()
    assert len(admins) == len(admins)


async def test_bulk_create_users(user_dal: UserDAL, session: AsyncSession, mock_users_list: list[dict[str, Any]]):
    """Test bulk creating users and verify with a direct database query."""    
    await user_dal.bulk_create(mock_users_list)
    
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    db_users = result.scalars().all()

    assert len(db_users) == len(mock_users_list)
    for mock_user, db_user in zip(mock_users_list, db_users):
        assert mock_user["username"] == db_user.username
        assert mock_user["email"] == db_user.email
        assert mock_user["password_hash"] == db_user.password_hash
        assert mock_user["is_superuser"] == db_user.is_superuser


async def test_get_all_users(user_dal: UserDAL, session: AsyncSession, create_mock_users, mock_users_list: list[dict[str, Any]]):
    """Test retrieving all users and verify with a direct database query."""

    db_users = await user_dal.get_all()

    assert len(mock_users_list) == len(db_users)


async def test_get_or_create_user(user_dal: UserDAL, session: AsyncSession, mock_user: dict[str, Any]):
    """Test get_or_create method and verify."""

    db_user = await user_dal.get_or_create(**mock_user)

    assert db_user is not None
    assert db_user.username == mock_user["username"]
    assert db_user.email == mock_user["email"]

    existing_user = await user_dal.get_or_create(**mock_user)
    assert existing_user.id == db_user.id

    stmt = select(User).where(User.username == mock_user["username"])
    result = await session.execute(stmt)
    users_with_same_name = result.scalars().all()

    assert len(users_with_same_name) == 1