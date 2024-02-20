from datetime import datetime
from typing import Any
from pydantic import BaseModel


class VocabularyAdminSchema(BaseModel):
    name: str
    created_at: datetime
    owner: Any
    is_active: bool = False
    language_pairs: list[Any] = None


class LanguagePairAdminSchema(BaseModel):
    vocabulary: Any
    word: str
    translation: str