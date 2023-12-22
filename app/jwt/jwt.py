from datetime import (
    datetime,
    timedelta,
)

from jose import (
    JWTError,
    jwt,
)

from app.config import settings
from app.jwt.exceptions import (
    JWTExpiredError,
    JwtMissingError,
    JwtNotValidError,
)


class JwtService:
    @staticmethod
    def _get_expire_time(exp_minutes=settings.JWT_EXPIRE_MINUTES) -> datetime:
        return datetime.utcnow() + timedelta(minutes=int(exp_minutes))

    @staticmethod
    def _get_token_pattern() -> dict:
        # TODO: rebuild to pydantic schema
        return {
            "expire": None,
            "sub": None,
        }

    @staticmethod
    def _is_token_expired(payload: dict) -> bool:
        expire_at = payload.get("exp")

        if expire_at < datetime.utcnow().timestamp():
            return True
        return False

    @classmethod
    def create_token(cls, data: str, expire: datetime | None = None) -> str:
        if not expire:
            expire: datetime = cls._get_expire_time()

        token_data: dict = cls._get_token_pattern()

        token_data.update({"exp": expire})
        token_data.update({"sub": data})

        encoded_token: str = jwt.encode(
            token_data,
            settings.JWT_SECRET,
            "HS256",
        )

        return encoded_token

    @classmethod
    def read_token(cls, token: str) -> dict:
        if not token:
            raise JwtMissingError

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                "HS256",
            )
        except JWTError:
            raise JwtNotValidError

        expired = cls._is_token_expired(payload)
        if expired:
            raise JWTExpiredError

        return payload