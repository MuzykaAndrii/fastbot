from typing import Any

from app.backend.users.services import UserService


async def test_get_or_create_by_id(user_service: UserService, mock_user: dict[str, Any], clean_db):
    # Act
    user = await user_service.get_or_create_by_id(mock_user["id"])
    
    # Assert
    assert user is not None
    assert user.id == mock_user["id"]