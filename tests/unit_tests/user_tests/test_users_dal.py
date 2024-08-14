from app.backend.users.dal import UserDAL


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