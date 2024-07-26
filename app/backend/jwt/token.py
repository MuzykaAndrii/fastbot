from datetime import UTC, datetime
from typing import Any


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