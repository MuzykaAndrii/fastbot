from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base
if TYPE_CHECKING:
    from app.users.models import User


class VocabularyBundle(Base):
    __tablename__ = 'vocabulary_bundles'
    id: Mapped[int] = mc(Integer, primary_key=True)

    owner_id: Mapped[int] = mc(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(
        back_populates="vocabulary_bundles",
        lazy="selectin",
    )

    name: Mapped[str] = mc(String(50), nullable=False)
    is_active: Mapped[bool] = mc(Boolean, nullable=False, default=False)

    word_pairs: Mapped[list["WordPair"]] = relationship(
        back_populates="bundle",
        cascade="all, delete-orphan",
    )


class WordPair(Base):
    __tablename__ = 'word_pairs'
    id: Mapped[int] = mc(Integer, primary_key=True)
    
    bundle_id: Mapped[int] = mc(ForeignKey("vocabulary_bundles.id"), nullable=False)
    bundle: Mapped[VocabularyBundle] = relationship(
        back_populates="word_pairs",
        lazy="selectin",
    )

    word: Mapped[str] = mc(String(100), nullable=False)
    translation: Mapped[str] = mc(String(100), nullable=False)