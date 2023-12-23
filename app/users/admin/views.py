from fastapi import Request
from starlette_admin.fields import StringField

from app.admin.view_overriding import MyModelView
from app.users.admin.schemas import UserCreateAdminSchema
from app.users.models import User
from app.users.services.pwd import PWDService


class UserAdminView(MyModelView):
    def __init__(self, *args, **kwargs):
        model = User
        pydantic_model = UserCreateAdminSchema
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
        StringField(
            "password_hash",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
            disabled=True,
            input_type="hidden",
            label="",
        ),
        User.is_superuser,
    ]

    def on_before_create(self, request: Request, data: dict) -> dict:
        raw_password = data.get("password")
        password_hash = PWDService.get_password_hash(raw_password)

        data.update({"password_hash": password_hash})
        data.pop("password", None)

        return data