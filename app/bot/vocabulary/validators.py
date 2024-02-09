import re


class VocabularyValidator:
    line_vocabulary_pattern = re.compile(r'^\s*([^-\n]+)\s*-\s*([^-\n]+[^\s])\s*$', re.I|re.X|re.S|re.U)

    def __init__(
            self,
            min_lines: int = 2,
            max_lines: int = 30,
            split_rule: str = "\n"
        ) -> None:
        self._min_lines = min_lines
        self._max_lines = max_lines
        self._split_rule = split_rule

    def validate(self, bulk_vocabulary: str) -> bool:
        raw_language_pairs = bulk_vocabulary.split(self._split_rule)
        language_pairs_count = len(raw_language_pairs)

        if language_pairs_count > self._max_lines or language_pairs_count < self._min_lines:
            return False
        
        is_all_lines_valid = all(self.validate_line(lang_pair) for lang_pair in raw_language_pairs)
        return is_all_lines_valid
    
    def validate_line(self, raw_lang_pair: str):
        if self.line_vocabulary_pattern.match(raw_lang_pair) is None:
            return False
        else:
            return True