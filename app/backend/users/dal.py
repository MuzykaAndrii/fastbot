from typing import Iterable

from app.backend.db.dal import BaseDAL
from app.backend.users.models import User


class UserDAL(BaseDAL[User]):
    model = User

    async def get_admin_users(self) -> Iterable[User] | None:
        admin_users = await self.filter_by(is_superuser=True)
        return admin_users