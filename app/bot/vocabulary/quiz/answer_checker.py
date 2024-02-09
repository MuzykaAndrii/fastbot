import re

from app.bot.modules.string_matcher.string_matcher import StringMatcher


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
        text: str = text.strip().lower()
        text: set[str] = set(self._split_text(text))
        text: tuple[StringMatcher] = tuple(StringMatcher(variant, self.accuracy) for variant in text)
        return text

    def _trim_parenthesis(self, text: str) -> str:
        return re.sub(r"\([^)]*\)", '', text)

    def _split_text(self, text: str) -> list[str]:
        return re.split(r"\s*,\s*", text)
    
    def __str__(self) -> str:
        return " | ".join(str(variant) for variant in self._variants)


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

    assert QuizAnswerChecker("грубий (про стан якоїсь речі)", "Грубий").is_match() == True