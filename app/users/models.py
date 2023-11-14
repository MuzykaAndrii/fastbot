from sqlalchemy import (
    Boolean,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(Integer, primary_key=True)
    tg_id: Mapped[int] = mc(Integer, unique=True, index=True, nullable=False)
    username: Mapped[str] = mc(String(length=50), nullable=True)
    email: Mapped[str] = mc(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mc(String, nullable=True)

    is_superuser: Mapped[bool] = mc(Boolean, default=False, nullable=False)