from difflib import SequenceMatcher
from typing import Union


class StringMatcher:
    def __init__(self, text: str, similarity_treshold: float = .95) -> None:
        self._text = text
        self.similarity_treshold = similarity_treshold
    
    @property
    def text(self) -> str:
        return self._text

    def __eq__(self, other: Union[str, "StringMatcher"]) -> bool:
        match other:
            case str():
                to_compare = other
            case StringMatcher():
                to_compare = other.text
            case _:
                raise TypeError
            
        return SequenceMatcher(None, self._text, to_compare).ratio() >= self.similarity_treshold

    def __str__(self) -> str:
        return str(self._text)