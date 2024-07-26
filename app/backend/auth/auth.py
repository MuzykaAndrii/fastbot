from fastapi import Response

from app.backend.jwt.exceptions import MyJwtError
from app.backend.jwt.interface import IJwt
from .cookie import AuthCookieManager
from .schemas import UserLogin
from .exceptions import AuthenticationError, InvalidUserIdError, UserInvalidPassword, UserNotFoundError
from app.backend.users.models import User
from app.backend.pwd import PWDService
from app.backend.components.services import users_service

"""
dependencies:
- jwt access token
- users service
- password manager
- cookie manager
"""

class AuthService:
    def __init__(self, jwt: IJwt) -> None:
        self.jwt = jwt

    async def authenticate_user(self, user_in: UserLogin) -> User:
        user = await users_service().get_by_email(user_in.email)

        if not user:
            raise UserNotFoundError

        pass_matching = PWDService.verify_password(
            raw_password=user_in.password, hashed_password=user.password_hash
        )

        if not pass_matching:
            raise UserInvalidPassword

        return user
    
    async def get_user_from_token(self, token: str) -> User | None:
        try:
            payload = self.jwt.read(token)
        except MyJwtError as e:
            raise e

        try:
            user_id = int(payload.sub)
        except ValueError:
            raise InvalidUserIdError

        user = await users_service().get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        return user
    
    def set_auth_cookie(self, response_obj: Response, user_id: int) -> str:
        auth_token = self.jwt.create(str(user_id))
        AuthCookieManager().set_cookie(response_obj, auth_token)

        return auth_token
    
    async def login_user(self, response_obj: Response, user_in: UserLogin) -> User:
        try:
            user = await self.authenticate_user(user_in)
        except AuthenticationError as error:
            raise error

        self.set_auth_cookie(response_obj, user.id)

        return user


    def logout_user(self, response: Response) -> Response:
        return AuthCookieManager().delete_cookie(response)