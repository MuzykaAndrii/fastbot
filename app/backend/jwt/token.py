from datetime import UTC, datetime
from typing import Any


class Token:
    def __init__(self, sub: Any, exp: datetime) -> None:
        self.sub = sub
        self.exp = exp
    
    @property
    def is_expired(self):
        return self.exp < datetime.now(UTC).timestamp()
    
    def as_dict(self):
        return {
            "sub": self.sub,
            "exp": self.exp,
        }