from app.users.dal import UserDAL
from app.users.models import User


class UserService:

    @staticmethod
    async def get_or_create_by_id(id: int) -> User:
        user = await UserDAL.get_or_create(id=id)

        return user
    
    @staticmethod
    async def get_by_id(id: int) -> User:
        user = await UserDAL.get_one(id=id)
        return user
    
    @staticmethod
    async def get_by_email(email: str) -> User:
        return await UserDAL.get_one(email=email)