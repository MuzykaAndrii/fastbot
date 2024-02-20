from fastapi import Depends, HTTPException, Request
from app.backend.jwt import Jwt
from app.backend.jwt.exceptions import JWTExpiredError, JwtNotValidError
from app.backend.users.dal import UserDAL

from app.backend.users.models import User
from .cookie import AuthCookieManager


def get_auth_token(request: Request) -> str:
    auth_token = AuthCookieManager().get_cookie(request)

    if not auth_token:
        raise HTTPException(status_code=401)
    return auth_token


async def get_current_user(token: str = Depends(get_auth_token)) -> User:
    try:
        payload = Jwt.read_token(token)
        user_id = int(payload.get("sub"))
        user = await UserDAL.get_by_id(user_id)

    except (JwtNotValidError, JWTExpiredError, ValueError):
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=401)

    return user