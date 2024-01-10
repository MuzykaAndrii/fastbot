from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LanguagePairSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    word: str
    translation: str


class ExtendedLanguagePairSchema(BaseModel):
    word: str
    translation: str
    owner_id: int
    sentence_example: str | None = None


class VocabularySchema(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    language_pairs: list[LanguagePairSchema]


class VocabularyCreateSchema(BaseModel):
    owner_id: int
    name: str
    language_pairs: list[LanguagePairSchema]


class LanguagePairsAppendSchema(BaseModel):
    user_id: int
    vocabulary_id: int
    language_pairs: list[LanguagePairSchema]