from app.config import settings
from app.jwt.exceptions import JWTExpiredError, JwtNotValidError
from app.jwt import Jwt
from app.users.dal import UserDAL
from app.users.exceptions import InvalidUserIdError, UserNotFoundError
from app.users.models import User
from app.pwd import PWDService


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

    @classmethod
    async def ensure_admin_exists(cls) -> None:
        """Ensures the existence of at least one admin user in the system.
        If no admin users are found, creates a base admin user
        """
        admin_users = await UserDAL.get_admin_users()

        if not admin_users:
            await cls._create_base_admin_user()
    
    @staticmethod
    async def get_user_from_token(token: str) -> User | None:
        try:
            payload: dict = Jwt.read_token(token)
        except JwtNotValidError:
            raise JwtNotValidError
        except JWTExpiredError:
            raise JWTExpiredError

        try:
            user_id = int(payload.get("sub"))
        except ValueError:
            raise InvalidUserIdError

        user: User = await UserDAL.get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        return user

    @staticmethod
    def user_is_admin(user: User) -> bool:
        return user.is_superuser
    
    @classmethod
    async def _create_base_admin_user(cls) -> None:
        await UserDAL.create(
            email=settings.BASE_ADMIN_EMAIL,
            password_hash=PWDService.get_password_hash(settings.BASE_ADMIN_PASS),
            is_superuser=True,
        )