from sqlalchemy import insert
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
    await user_dal.session.commit()

    assert user.id is not None
    assert user.username == new_user["username"]
    assert user.email == new_user["email"]
    assert user.password_hash == new_user["password_hash"]
    assert user.is_superuser == new_user["is_superuser"]


async def test_get_user_by_id(user_dal: UserDAL, session: AsyncSession):
    vals = {"username": "testuser1", "email": "test1@example.com", "password_hash": b"hashed_pwd"}
    stmt = insert(User).values(**vals).returning(User)
    result = await session.execute(stmt)
    await session.commit()
    user = result.scalar_one()

    fetched_user = await user_dal.get_by_id(user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.username == vals["username"]
    assert fetched_user.email == vals["email"]
    assert fetched_user.password_hash == vals["password_hash"]