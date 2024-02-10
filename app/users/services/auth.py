from app.users.exceptions import UserInvalidPassword, UserNotFoundError
from app.users.models import User
from app.users.schemas import UserLogin
from app.pwd import PWDService
from app.users.services.user import UserService


class AuthService:
    @staticmethod
    async def authenticate_user(user_in: UserLogin) -> User:
        user = await UserService.get_by_email(user_in.email)

        if not user:
            raise UserNotFoundError

        pass_matching = PWDService.verify_password(
            raw_password=user_in.password, hashed_password=user.password_hash
        )

        if not pass_matching:
            raise UserInvalidPassword

        return user