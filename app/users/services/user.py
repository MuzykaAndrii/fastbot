from app.users.dal import UserDAL
from app.users.models import User


class UserService:

    @staticmethod
    async def get_or_create_from_tg_id(tg_id: int) -> User:
        user = await UserDAL.get_or_create(tg_id=tg_id)

        return user