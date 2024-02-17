from app.cookie.cookie import CookieManager
from app import config


class AuthCookieManager(CookieManager):
    def __init__(self) -> None:
        super().__init__(config.AUTH_TOKEN_NAME)