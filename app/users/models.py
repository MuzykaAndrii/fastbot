from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base
from app.words.models import VocabularySet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(Integer, primary_key=True)
    tg_id: Mapped[int] = mc(Integer, unique=True, index=True, nullable=False)
    username: Mapped[str] = mc(String(length=50), nullable=True)
    email: Mapped[str] = mc(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mc(String, nullable=True)

    vocabulary_sets: Mapped[list["VocabularySet"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    is_superuser: Mapped[bool] = mc(Boolean, default=False, nullable=False)