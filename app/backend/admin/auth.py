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
from app.backend.auth.auth import AuthService
from app.backend.auth.cookie import AuthCookieManager
from app.backend.auth.exceptions import AuthenticationError, UserInvalidPassword, UserNotFoundError
from app.backend.auth.schemas import UserLogin
from app.backend.jwt.exceptions import MyJwtError

from app.users.services import UserService


class AdminAuthProvider(AuthProvider):
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
                email=username,
                password=password,
            )
        except ValidationError:
            raise FormValidationError({"failed": "Invalid input data"})

        try:
            await AuthService.login_user(response, credentials)
        except UserNotFoundError:
            raise LoginFailed("user not found")
        except UserInvalidPassword:
            raise LoginFailed("Invalid password")

        return response

    async def is_authenticated(self, request: Request) -> bool:
        token = AuthCookieManager().get_cookie(request)

        try:
            current_user = await AuthService.get_user_from_token(token)
        except (MyJwtError, AuthenticationError):
            return False

        if not UserService.user_is_admin(current_user):
            return False

        request.state.user = current_user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user

        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        AuthService.logout_user(response)
        return response