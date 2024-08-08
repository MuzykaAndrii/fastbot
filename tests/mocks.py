


def get_mock_users_data():
    return (
        {
            "username": "testuser",
            "email": "testuser@example.com",
            "password_hash": b"hashedpassword",
            "is_superuser": False,
        },
        {
            "username": "adminuser",
            "email": "admin@example.com",
            "password_hash": b"hashedpassword",
            "is_superuser": True,
        },
        {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password_hash": b"hashedpassword",
            "is_superuser": False,
        },
        {
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password_hash": b"hashedpassword",
            "is_superuser": False,
        },
    )