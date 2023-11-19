from pydantic import BaseModel


class LanguagePairSchema(BaseModel):
    word: str
    translation: str


class VocabularySetSchema(BaseModel):
    id: int
    name: str
    is_active: bool
    language_pairs: list[LanguagePairSchema]