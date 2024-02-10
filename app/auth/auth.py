from app.jwt import jwt
from app.jwt.exceptions import JWTExpiredError, JwtNotValidError
from app.users.dal import UserDAL
from .exceptions import InvalidUserIdError, UserInvalidPassword, UserNotFoundError
from app.users.models import User
from .schemas import UserLogin
from app.pwd import PWDService
from app.users.services import UserService


class AuthService:
    @classmethod
    async def authenticate_user(cls, user_in: UserLogin) -> User:
        user = await UserService.get_by_email(user_in.email)

        if not user:
            raise UserNotFoundError

        pass_matching = PWDService.verify_password(
            raw_password=user_in.password, hashed_password=user.password_hash
        )

        if not pass_matching:
            raise UserInvalidPassword

        return user
    
    @classmethod
    async def get_user_from_token(cls, token: str) -> User | None:
        try:
            payload: dict = jwt.read_token(token)
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
    
    # @classmethod
    # async def login_user(cls, response_obj: Response, user_in: UserLogin) -> Response:
    #     try:
    #         user = await cls.authenticate_user(user_in)
    #     except UserLoginError as error:
    #         raise error

    #     login_response = set_auth_cookie(response_obj, user.id)

    #     return login_response


    # async def logout_user(response: Response) -> Response:
    #     return AuthCookieManager().delete_cookie(response)