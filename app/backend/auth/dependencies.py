from fastapi import Depends, HTTPException, Request

from app.backend.auth.schemas import ApiKeyAuthorizationSchema
from app.backend.jwt.exceptions import MyJwtError
from app.backend.users.models import User
from .auth import AuthService
from app.backend.components import auth_cookie_manager
from .exceptions import InvalidUserIdError, UserNotFoundError
from app.backend.components.config import auth_settings


def api_key_auth(auth: ApiKeyAuthorizationSchema):
    if auth.api_key != auth_settings.API_KEY:
        raise HTTPException(401, detail="Invalid API key")
    
# FIX: NEED TO BE FIXED

def get_auth_token(request: Request) -> str:
    auth_token = auth_cookie_manager.get_cookie(request)

    if not auth_token:
        raise HTTPException(status_code=401)
    return auth_token


async def get_current_user(token: str = Depends(get_auth_token)) -> User:    
    try:
        return await AuthService.get_user_from_token(token)
    except (MyJwtError, InvalidUserIdError, UserNotFoundError):
        raise HTTPException(status_code=401)
