from fastapi import Request
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from app.backend.db.base import Base
from app.backend.vocabulary.models import VocabularySet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(Integer, primary_key=True)
    username: Mapped[str] = mc(String(length=50), nullable=True)
    email: Mapped[str] = mc(String, unique=True, nullable=True)
    password_hash: Mapped[bytes] = mc(LargeBinary, nullable=True)

    vocabulary_sets: Mapped[list["VocabularySet"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    is_superuser: Mapped[bool] = mc(Boolean, default=False, nullable=False)

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}"

    def __repr__(self):
        return (f"User(id={self.id}, username={repr(self.username)}, "
                f"email={repr(self.email)}, is_superuser={self.is_superuser})")
    
    def __admin_repr__(self, request: Request) -> str:
        return f"{self.id}"