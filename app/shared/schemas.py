from pydantic import BaseModel


class ExtendedLanguagePairSchema(BaseModel):
    word: str
    translation: str
    owner_id: int
    sentence_example: str | None = None