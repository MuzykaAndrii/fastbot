from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LanguagePairSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vocabulary_id: int
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