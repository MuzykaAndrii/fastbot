import re


class VocabularyValidator:
    line_vocabulary_pattern = re.compile(r'^\s*([^-\n]+)\s*-\s*([^-\n]+[^\s])\s*$', re.I|re.X|re.S|re.U)

    @classmethod
    def validate_bulk(cls, bulk_vocabulary: str) -> bool:
        raw_language_pairs = bulk_vocabulary.split("\n")

        if len(raw_language_pairs) < 2:
            return False
        
        if all(cls.validate_line(lang_pair) for lang_pair in raw_language_pairs):
            return True
        
        return False
    
    @classmethod
    def validate_line(cls, raw_lang_pair: str):
        if cls.line_vocabulary_pattern.match(raw_lang_pair) is None:
            return False
        else:
            return True