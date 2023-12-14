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


class QuizAnswerChecker:
    def __init__(
            self,
            suggested_translation: str,
            correct_translation: str,
            similarity_ratio_treshold: float = .95,
            variants_separator: str = ","
    ) -> None:
        self.suggested_translation = suggested_translation.strip().lower()
        self.correct_translation = self._trim_parenthesis(correct_translation).strip().lower()
        self._similarity_ratio_treshold = similarity_ratio_treshold
        self._variants_separator = variants_separator
    
    def is_match(self) -> bool:
        if self._variants_separator in self.suggested_translation:
            return self.check_full_similarity()
        else:
            return self.check_partial_similarity()
    
    def check_full_similarity(self) -> bool:
        return self._is_suggested_translation_match(self.suggested_translation, self.correct_translation)
    
    def check_partial_similarity(self) -> bool:
        correct_translation_variants = self._get_correct_translation_variants()

        for variant in correct_translation_variants:
            if self._is_suggested_translation_match(self.suggested_translation, variant):
                return True
        return False

    def _get_correct_translation_variants(self) -> list[str]:
        return re.split(r"\s*,\s*", self.correct_translation)

    def _is_suggested_translation_match(self, suggested_translation: str, correct_translation: str) -> bool:
        similarity = SequenceMatcher(None, suggested_translation, correct_translation).ratio()

        return similarity >= self._similarity_ratio_treshold

    def _trim_parenthesis(self, text: str) -> str:
        pattern = r'\([^)]*\)'
        return re.sub(pattern, '', text)
    