import pytest

from app.bot.vocabulary.validators import VocabularyValidator


@pytest.fixture
def validator():
    return VocabularyValidator(min_lines=2, max_lines=5)

@pytest.mark.parametrize("bulk_vocabulary, expected", [
    # Valid cases
    ("apple - manzana\nbanana - plátano", True),  # Exactly 2 lines (valid)
    ("apple - manzana\nbanana - plátano\norange - naranja\npear - pera\nkiwi - kiwi", True),  # Exactly 5 lines (valid)
    ("apple - manzana\nbanana - plátano", True),  # Normal case
    ("apple   -   manzana\nbanana- plátano", True),  # Extra spaces
    ("apple - manzana\nbanana - plátano\norange - naranja\npear - pera\nkiwi - kiwi", True),  # Max lines boundary
    ("HELLO - HOLA\nWORLD - MUNDO", True),  # Uppercase terms
    ("   apple   -   manzana\nbanana - plátano    ", True),  # Leading and trailing spaces

    # Invalid cases
    ("", False),  # empty line
    ("   \n   ", False),  # whitespaces only input
    ("apple - manzana", False),  # Only 1 line (invalid)
    ("apple - manzana\nbanana - plátano\norange - naranja\npear - pera\nkiwi - kiwi\nextra - línea", False),  # 6 lines (invalid)
    ("mother-in-law - suegra\nbanana - plátano", False),  # Hyphen in terms, need to fix this to true
    ("apple manzana\nbanana - plátano", False),  # Missing hyphen
    ("apple -\nbanana - plátano", False),  # Missing second word
    (" - manzana\nbanana - plátano", False),  # Missing first word
    ("apple - manzana\nbanana - plátano\norange - naranja\npear - pera\nkiwi - kiwi\nextra - línea", False),  # Exceeding max lines
    ("apple-", False),  # No second term
    ("apple - \n - ", False),  # Both terms missing in one line
    (" - ", False),  # Only hyphen with no terms
    ("apple - manzana\n\n", False),  # Empty second line
    ("apple -- manzana", False),  # Multiple consecutive hyphens
    ("- apple\nbanana - plátano", False),  # Hyphen at the start
    ("apple - manzana-", False),  # Hyphen at the end
    ("1234 - mil doscientos treinta y cuatro\nbanana - plátano", False),  # Numbers as invalid first term
    ("apple -1234", False),  # Numbers as invalid second terms
])
def test_vocabulary_validator(bulk_vocabulary, expected, validator: VocabularyValidator):
    assert validator.validate(bulk_vocabulary) == expected


@pytest.mark.parametrize("line, expected", [
    ("sophisticated, subtle - витончений", True),  # cyrillic symbols allowed
    ("one, another - third", True),  # divided by coma in left
    ("one - third, another", True),  # divided by comma in right
    ("one (someone) - another", True),  # parenthesis in left
    ("one - another (third)", True),  # parenthesis in right
    ("one - another, third (extra)", True),  # parenthesis and divided by comma in right
    ("one, second (third) - another", True),  # parenthesis and divided by comma in left
    ("one, two (third) - another, second (extra)", True),  # parenthesis and divided by coma in both sides
    ("one, two, extraf, extras (comment in left) - another, second, extrat (comment in right)", True),  # parenthesis and multiply divided by coma in both sides
])
def test_vocabulary_validator_comments_and_commas(line, expected, validator):
    assert validator.validate_line(line) == expected