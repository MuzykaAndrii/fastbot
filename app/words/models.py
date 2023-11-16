from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

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
    is_active: Mapped[bool] = mc(Boolean, nullable=False, default=False)

    language_pairs: Mapped[list["LanguagePair"]] = relationship(
        back_populates="vocabulary",
        cascade="all, delete-orphan",
    )


class LanguagePair(Base):
    __tablename__ = 'language_pairs'
    id: Mapped[int] = mc(Integer, primary_key=True)
    
    vocabulary_id: Mapped[int] = mc(ForeignKey("vocabulary_sets.id"), nullable=False)
    vocabulary: Mapped[VocabularySet] = relationship(
        back_populates="language_pairs",
        lazy="selectin",
    )

    word: Mapped[str] = mc(String(100), nullable=False)
    translation: Mapped[str] = mc(String(100), nullable=False)