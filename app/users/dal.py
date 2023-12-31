from typing import Iterable

from app.db.dal import BaseDAL
from app.users.models import User


class UserDAL(BaseDAL):
    model = User

    @classmethod
    async def get_admin_users(cls) -> Iterable[User] | None:
        admin_users = await cls.filter_by(is_superuser=True)
        return admin_users