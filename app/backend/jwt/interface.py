from typing import Any
from abc import ABC, abstractmethod


class IJwtEncoder(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, raw_token: str) -> dict:
        pass


class IJwt(ABC):
    @abstractmethod
    def create(self, sub: Any) -> str:
        pass

    @abstractmethod
    def read(self, encoded_token: str) -> Any:
        pass