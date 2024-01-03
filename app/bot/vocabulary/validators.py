import re
from difflib import SequenceMatcher


class VocabularyValidator:
    line_vocabulary_pattern = re.compile(r'^\s*([^-\n]+)\s*-\s*([^-\n]+[^\s])\s*$', re.I|re.X|re.S|re.U)

    @classmethod
    def validate_bulk(cls, bulk_vocabulary: str) -> bool:
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

# TODO: divide class below into two classes
class StringMatcher:
    def __init__(self, text: str, similarity_ratio_treshold: float = .95) -> None:
        self._lines = self._clean_text(text)
        self.similarity_ratio_treshold = similarity_ratio_treshold

    def __contains__(self, to_compare: str) -> bool:
        for line in self._lines:
            if SequenceMatcher(None, to_compare, line).ratio() >= self.similarity_ratio_treshold:
                return True
        return False
    
    @property
    def lines(self) -> list[str]:
        return self._lines
    
    def _clean_text(self, text: str) -> list[str]:
        text: str = text.strip().lower()
        text: str = self._trim_parenthesis(text)
        text: list[str] = self._split_text(text)
        return text

    def _trim_parenthesis(self, text: str) -> str:
        return re.sub(r"\([^)]*\)", '', text)

    def _split_text(self, text: str) -> list[str]:
        return re.split(r"\s*,\s*", text)


class QuizAnswerChecker:
    def __init__(self, suggested_translation: str, correct_translation: str) -> None:
        self.suggested_translation = StringMatcher(suggested_translation)
        self.correct_translation = StringMatcher(correct_translation)
    
    def is_match(self) -> bool:
        return all(suggested in self.correct_translation for suggested in self.suggested_translation.lines)


if __name__ == '__main__':
    assert QuizAnswerChecker("винний, зобовязаний", "зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("зобовязаний, винний", "зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("зобовязаний, винний, ще якись", "зобовязаний, винний").is_match() == False

    assert QuizAnswerChecker("зобовязаний, винний, ще якись", "ще якись, зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker(",", "ще якись, зобовязаний, винний").is_match() == False
    assert QuizAnswerChecker("зобовязаний,", "ще якись, зобовязаний, винний").is_match() == False

    assert QuizAnswerChecker("зобовязаний, винний", "ще якись, зобовязаний, винний").is_match() == True
    assert QuizAnswerChecker("винний, зобовязаний", "ще якись, зобовязаний, винний").is_match() == True
