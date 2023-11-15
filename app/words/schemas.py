from dataclasses import dataclass


@dataclass
class VocabularyUnitSchema:
    word: str
    translation: str