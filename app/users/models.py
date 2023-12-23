from sqlalchemy import (
    Boolean,
    Integer,
    String,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base
from app.vocabulary.models import VocabularySet


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