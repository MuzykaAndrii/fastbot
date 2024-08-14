from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.users.dal import UserDAL
from app.backend.users.models import User


async def test_create_user(user_dal: UserDAL):
    """Test creating a new user."""
    new_user = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password_hash": b"somehashedpassword",
        "is_superuser": False,
    }
    user = await user_dal.create(**new_user)

    assert user.id is not None
    assert user.username == new_user["username"]
    assert user.email == new_user["email"]
    assert user.password_hash == new_user["password_hash"]
    assert user.is_superuser == new_user["is_superuser"]


async def test_get_user_by_id(user_dal: UserDAL, session: AsyncSession):
    vals = {"username": "testuser1", "email": "test1@example.com", "password_hash": b"hashed_pwd"}
    stmt = insert(User).values(**vals).returning(User)
    result = await session.execute(stmt)
    user = result.scalar_one()

    fetched_user = await user_dal.get_by_id(user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.username == vals["username"]
    assert fetched_user.email == vals["email"]
    assert fetched_user.password_hash == vals["password_hash"]


async def test_bulk_create_users(user_dal: UserDAL, session: AsyncSession):
    mock_users = [
        {"username": "user1", "email": "user1@example.com", "password_hash": b"pwd1"},
        {"username": "user2", "email": "user2@example.com", "password_hash": b"pwd2"},
    ]
    
    for mock_user in mock_users:
        stmt = insert(User).values(**mock_user).returning(User)
        await session.execute(stmt)


    users = await user_dal.get_all()
    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"


async def test_delete_user_by_id(user_dal: UserDAL, session: AsyncSession):
    vals = {"username": "testuser", "email": "test@example.com", "password_hash": b"hashed_pwd"}
    stmt = insert(User).values(**vals).returning(User)
    result = await session.execute(stmt)
    user = result.scalar_one()

    deleted_user = await user_dal.delete_by_id(user.id)

    assert deleted_user.id == user.id

    # Verify that the user no longer exists in the database
    stmt = select(User).where(User.id == user.id)
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is None


async def test_filter_users_by_criteria(user_dal: UserDAL, session: AsyncSession):
    """Test filtering users by criteria."""
    users_list = [
        {"username": "user1", "email": "user1@example.com", "password_hash": b"pwd1"},
        {"username": "admin", "email": "admin@example.com", "password_hash": b"pwd2", "is_superuser": True},
    ]
    
    for user in users_list:
        stmt = insert(User).values(**user).returning(User)
        await session.execute(stmt)


    found = await user_dal.filter_by(**users_list[1])
    assert len(found) == 1


async def test_get_admin_users(user_dal: UserDAL, session: AsyncSession):
    """Test getting all admin users."""
    mock_users = [
        {"username": "user1", "email": "user1@example.com", "password_hash": b"pwd1"},
        {"username": "admin", "email": "admin@example.com", "password_hash": b"pwd2", "is_superuser": True},
    ]
    
    for mock_user in mock_users:
        stmt = insert(User).values(**mock_user).returning(User)
        await session.execute(stmt)

    admins = await user_dal.get_admin_users()
    assert len(admins) == 1
    assert admins[0].username == "admin"


async def test_bulk_create_users(user_dal: UserDAL, session: AsyncSession):
    """Test bulk creating users and verify with a direct database query."""
    mock_users = [
        {"username": "user1", "email": "user1@example.com", "password_hash": b"pwd1"},
        {"username": "user2", "email": "user2@example.com", "password_hash": b"pwd2"},
    ]
    
    await user_dal.bulk_create(mock_users)
    
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    db_users = result.scalars().all()

    assert len(db_users) == len(mock_users)
    for mock_user, db_user in zip(mock_users, db_users):
        assert mock_user["username"] == db_user.username
        assert mock_user["email"] == db_user.email


