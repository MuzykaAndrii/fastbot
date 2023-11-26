from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.sql import func

from app.db.base import Base
if TYPE_CHECKING:
    from app.users.models import User


class VocabularySet(Base):
    __tablename__ = 'vocabulary_sets'
    id: Mapped[int] = mc(Integer, primary_key=True)

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
        return f"Vocabulary set: {self.name} with: {self.language_pairs}"
    
    def __repr__(self) -> str:
        return str(self)


class LanguagePair(Base):
    __tablename__ = 'language_pairs'
    id: Mapped[int] = mc(Integer, primary_key=True)
    
    vocabulary_id: Mapped[int] = mc(ForeignKey("vocabulary_sets.id", ondelete="CASCADE"), nullable=False)
    vocabulary: Mapped[VocabularySet] = relationship(
        back_populates="language_pairs",
        lazy="selectin",
    )

    word: Mapped[str] = mc(String(100), nullable=False)
    translation: Mapped[str] = mc(String(100), nullable=False)

    def __str__(self) -> str:
        return f"Lang pair: {self.word} - {self.translation}"
    
    def __repr__(self) -> str:
        return str(self)