from fastapi import Depends, HTTPException, Request

from app.backend.jwt.exceptions import MyJwtError
from app.backend.users.models import User
from .auth import AuthService
from .cookie import AuthCookieManager
from .exceptions import InvalidUserIdError, UserNotFoundError

# FIX: NEED TO BE FIXED

def get_auth_token(request: Request) -> str:
    auth_token = AuthCookieManager().get_cookie(request)

    if not auth_token:
        raise HTTPException(status_code=401)
    return auth_token


async def get_current_user(token: str = Depends(get_auth_token)) -> User:    
    try:
        return await AuthService.get_user_from_token(token)
    except (MyJwtError, InvalidUserIdError, UserNotFoundError):
        raise HTTPException(status_code=401)
