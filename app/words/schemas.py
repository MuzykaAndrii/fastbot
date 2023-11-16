from pydantic import BaseModel, ConfigDict


class LanguagePairSchema(BaseModel):
    model_config: ConfigDict(from_attributes=True)

    vocabulary_id: int
    word: str
    translation: str