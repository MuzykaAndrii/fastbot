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

from app.backend.auth.protocols import CookieManagerProtocol
from .protocols import AuthServiceProtocol
from app.backend.auth.exceptions import AuthenticationError, UserInvalidPassword, UserNotFoundError
from app.backend.auth.schemas import UserLogin
from app.backend.jwt.exceptions import MyJwtError


class AdminAuthProvider(AuthProvider):
    def __init__(self, auth_service: AuthServiceProtocol, auth_cookie_manager: CookieManagerProtocol, *args, **kwargs):
        self.auth_service = auth_service
        self.auth_cookie_manager = auth_cookie_manager
        super().__init__(*args, **kwargs)

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
            await self.auth_service.login_user(response, credentials)
        except UserNotFoundError:
            raise LoginFailed("user not found")
        except UserInvalidPassword:
            raise LoginFailed("Invalid password")

        return response

    async def is_authenticated(self, request: Request) -> bool:
        token = self.auth_cookie_manager.get_cookie(request)

        try:
            current_user = await self.auth_service.get_user_from_token(token)
        except (MyJwtError, AuthenticationError):
            return False

        if not current_user.is_superuser:
            return False

        request.state.user = current_user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user

        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        self.auth_service.logout_user(response)
        return response