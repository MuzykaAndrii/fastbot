from fastapi import (
    Request,
    Response,
)
from pydantic import ValidationError
from starlette_admin.auth import (
    AdminUser,
    AuthProvider,
)
from starlette_admin.exceptions import (
    FormValidationError,
    LoginFailed,
)

from app.jwt.exceptions import (
    JWTExpiredError,
    JwtMissingError,
    JwtNotValidError,
)
from app.jwt.jwt import Jwt
from app.users.exceptions import (
    InvalidUserIdError,
    UserInvalidPassword,
    UserNotFoundError,
)
from app.users.schemas import UserLogin
from app.users.services.auth import AuthService
from app.users.services.user import UserService


class AdminAuthProvider(AuthProvider):
    token_name: str = "auth_token"

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        try:
            credentials = UserLogin(
                username_or_email=username,
                password=password,
            )
        except ValidationError:
            raise FormValidationError({"failed": "Invalid input data"})

        try:
            user = await AuthService.authenticate_user(credentials)
        except UserNotFoundError:
            raise LoginFailed("Invalid username/email")
        except UserInvalidPassword:
            raise LoginFailed("Invalid password")

        auth_token = Jwt.create_token(str(user.id))
        request.session.update({self.token_name: auth_token})
        return response

    async def is_authenticated(self, request: Request) -> bool:
        token: str = request.session.get(self.token_name)

        try:
            current_user = await UserService.get_user_from_token(token)
        except (
            JwtMissingError,
            JwtNotValidError,
            JWTExpiredError,
            InvalidUserIdError,
            UserNotFoundError,
        ):
            return False

        if not UserService.user_is_admin(current_user):
            return False

        request.state.user = current_user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user

        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response