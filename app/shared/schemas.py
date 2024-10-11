from datetime import datetime
from pydantic import BaseModel, ConfigDict, validator


class LanguagePairSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vocabulary_id: int | None = None
    word: str
    translation: str


class NotificationSchema(BaseModel):
    primary_lp: LanguagePairSchema
    secondary_lp: LanguagePairSchema | None = None
    owner_id: int
    sentence_example: str | None = None


class VocabularySchema(BaseModel):
    id: int
    owner_id: int
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

    @validator("language_pairs", pre=True, each_item=True)
    def attach_vocabulary_id(cls, v: LanguagePairSchema, values: dict):
        v.vocabulary_id = values.get("vocabulary_id")
        return v