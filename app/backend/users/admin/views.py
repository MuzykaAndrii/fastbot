from typing import Any

from fastapi import Request
from starlette_admin.fields import StringField
from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from app.backend.users.admin.schemas import UserAdminSchema
from app.backend.users.models import User
from app.backend.components import pwd_service


class UserAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = User
        pydantic_model = UserAdminSchema
        icon = "fa-regular fa-user"
        name = "User"
        label = "Users"
        identity = None

        super().__init__(model, pydantic_model, icon, name, label, identity)

    fields = [
        User.id,
        User.username,
        User.email,
        StringField(
            "password",
            label="Password",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
        ),
        User.is_superuser,
    ]

    async def before_create(self, request: Request, data: dict[str, Any], user: User) -> None:
        raw_password = data.get("password")
        user.password_hash = pwd_service.get_hash(raw_password)