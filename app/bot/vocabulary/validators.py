import re
from difflib import SequenceMatcher
from typing import Union

from app.shared.schemas import LanguagePairSchema


class VocabularyParser:
    split_rule: str = r'\s*-\s*'

    def parse_bulk_vocabulary(self, raw_bulk_vocabulary: str) -> list[LanguagePairSchema]:
        lines = raw_bulk_vocabulary.split('\n')
        result: list[LanguagePairSchema] = []

        for line in lines:
            result.append(self.parse_line_vocabulary(line))

        return result
    
    def parse_line_vocabulary(self, raw_line_vocabulary: str) -> LanguagePairSchema:
        word, translation = re.split(self.split_rule, raw_line_vocabulary)

        return LanguagePairSchema(
            word=word.strip(),
            translation=translation.strip(),
        )


class VocabularyValidator:
    line_vocabulary_pattern = re.compile(r'^\s*([^-\n]+)\s*-\s*([^-\n]+[^\s])\s*$', re.I|re.X|re.S|re.U)

    @classmethod
    def validate(cls, bulk_vocabulary: str) -> bool:
        raw_language_pairs = bulk_vocabulary.split("\n")

        if len(raw_language_pairs) < 2:
            return False
        
        is_all_lines_valid = all(cls.validate_line(lang_pair) for lang_pair in raw_language_pairs)
        return is_all_lines_valid
    
    @classmethod
    def validate_line(cls, raw_lang_pair: str):
        if cls.line_vocabulary_pattern.match(raw_lang_pair) is None:
            return False
        else:
            return True


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


class TranslationChecker:
    def __init__(self, text: str, accuracy: float = .95) -> None:
        self.accuracy = accuracy
        self._variants = self._split_variants(text)

    def __contains__(self, to_compare: str | StringMatcher) -> bool:
        return any(translation == to_compare for translation in self)
    
    def __iter__(self):
        return iter(self._variants)

    def _split_variants(self, text: str) -> tuple[StringMatcher]:
        text: str = text.strip().lower()
        text: str = self._trim_parenthesis(text)
        text: set[str] = set(self._split_text(text))
        text: tuple[StringMatcher] = tuple(StringMatcher(variant, self.accuracy) for variant in text)
        return text

    def _trim_parenthesis(self, text: str) -> str:
        return re.sub(r"\([^)]*\)", '', text)

    def _split_text(self, text: str) -> list[str]:
        return re.split(r"\s*,\s*", text)


class QuizAnswerChecker:
    def __init__(self, suggested_translation: str, correct_translation: str) -> None:
        self.suggested_translation = TranslationChecker(suggested_translation)
        self.correct_translation = TranslationChecker(correct_translation)
    
    def is_match(self) -> bool:
        return all(suggested in self.correct_translation for suggested in self.suggested_translation)


if __name__ == '__main__':
    assert QuizAnswerChecker("винний, зобовязаний", "зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("зобовязаний, винний", "зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("зобовязаний, винний, ще якись", "зобовязаний, винний").is_match() == False

    assert QuizAnswerChecker("зобовязаний, винний, ще якись", "ще якись, зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker(",", "ще якись, зобовязаний, винний").is_match() == False
    assert QuizAnswerChecker("зобовязаний,", "ще якись, зобовязаний, винний").is_match() == False

    assert QuizAnswerChecker("зобовязаний, винний", "ще якись, зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("винний, зобовязаний", "ще якись, зобовязаний, винний").is_match() == True
