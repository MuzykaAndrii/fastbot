from app import config
from app.backend.cookie import CookieManager


class AuthCookieManager(CookieManager):
    def __init__(self) -> None:
        super().__init__(config.AUTH_TOKEN_NAME)