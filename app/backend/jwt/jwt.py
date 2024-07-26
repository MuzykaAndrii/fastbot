from abc import ABC, abstractmethod
from datetime import (
    datetime,
    timedelta,
    UTC,
)
from typing import Any

from jose import (
    JWTError,
    jwt,
)
from .exceptions import JWTExpiredError, JwtMissingError, JwtNotValidError


class Token:
    def __init__(self, sub: Any, expire: datetime) -> None:
        self.sub = sub
        self.expire = expire
    
    @property
    def is_expired(self):
        return self.expire < datetime.now(UTC).timestamp()
    
    def as_dict(self):
        return {
            "sub": self.sub,
            "exp": self.expire,
        }


class IJwtEncoder(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, raw_token: str) -> dict:
        pass


class JoseEncoder(IJwtEncoder):
    def __init__(self, key: str, alg: str = "HS256") -> None:
        self.key = key
        self.alg = alg
    
    def encode(self, payload: dict) -> str:
        return jwt.encode(
            payload,
            self.key,
            self.alg,
        )
    
    def decode(self, raw_token: str) -> dict:
        try:
            decoded = jwt.decode(
                raw_token,
                self.key,
                self.alg,
            )
        except JWTError:
            raise JwtNotValidError
        
        return decoded


class IJwt(ABC):
    @abstractmethod
    def create(self, sub: Any) -> str:
        pass

    @abstractmethod
    def read(self, encoded_token: str) -> Any:
        pass


class Jwt(IJwt):
    def __init__(self, encoder: IJwtEncoder, lifetime_minutes: datetime) -> None:
        self.lifetime_minutes = lifetime_minutes
        self._encoder = encoder
    
    def create(self, sub: Any) -> str:
        token = Token(
            sub=sub,
            expire=self._get_expire_time(),
        )

        return self._encoder.encode(token.as_dict())


    def _get_expire_time(self) -> datetime:
        return datetime.now(UTC) + timedelta(minutes=int(self.lifetime_minutes))

    def read(self, encoded_token: str) -> Token:
        if not encoded_token:
            raise JwtMissingError

        decoded = self._encoder.decode(encoded_token)
        token = Token(**decoded)
        
        if token.is_expired:
            raise JWTExpiredError
        
        return token