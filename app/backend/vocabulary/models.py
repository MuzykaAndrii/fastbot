from typing import TYPE_CHECKING
from datetime import datetime
from fastapi import Request

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.sql import func

from app.backend.db.base import Base
if TYPE_CHECKING:
    from app.backend.users.models import User


class VocabularySet(Base):
    __tablename__ = 'vocabulary_sets'

    owner_id: Mapped[int] = mc(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(
        back_populates="vocabulary_sets",
        lazy="selectin",
    )

    name: Mapped[str] = mc(String(50), nullable=False)
    created_at: Mapped[datetime] = mc(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mc(Boolean, nullable=False, default=False)

    language_pairs: Mapped[list["LanguagePair"]] = relationship(
        back_populates="vocabulary",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __str__(self) -> str:
        return f"Vocabulary: name={self.name}, is_active={self.is_active}, owner_id={self.owner_id}"

    def __repr__(self) -> str:
        return (f"VocabularySet(id={self.id}, name={repr(self.name)}, is_active={self.is_active}, created_at={repr(self.created_at)}, "
        f"owner_id={self.owner_id}, language_pairs={repr(self.language_pairs)})")
    
    def __admin_repr__(self, request: Request) -> str:
        return f"{self.name}"


class LanguagePair(Base):
    __tablename__ = 'language_pairs'
    
    vocabulary_id: Mapped[int] = mc(ForeignKey("vocabulary_sets.id", ondelete="CASCADE"), nullable=False)
    vocabulary: Mapped[VocabularySet] = relationship(
        back_populates="language_pairs",
        lazy="selectin",
    )

    word: Mapped[str] = mc(String(100), nullable=False)
    translation: Mapped[str] = mc(String(100), nullable=False)

    def __str__(self) -> str:
        return f"LanguagePair: id={self.id}, word={self.word}, translation={self.translation}, vocabulary_id={self.vocabulary_id})"

    def __repr__(self) -> str:
        return f"LanguagePair(id={self.id}, word={repr(self.word)}, translation={repr(self.translation)}, vocabulary_id={self.vocabulary_id})"
    
    def __admin_repr__(self, request: Request) -> str:
        return f"{self.word} - {self.translation}"