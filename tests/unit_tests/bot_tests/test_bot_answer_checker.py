import pytest

from app.bot.vocabulary.quiz.answer_checker import QuizAnswerChecker, TranslationChecker


@pytest.mark.parametrize(
    "suggested, correct, result",
    (
        ("зобовязаний", "зобовязаний", True),
        ("винний", "винний", True),
        
        # Tests with different cases
        ("Зобовязаний", "зобовязаний", True),
        ("ВИННИЙ", "винний", True),
        
        # Tests with leading/trailing whitespaces
        ("  зобовязаний  ", "зобовязаний", True),
        (" винний ", "винний", True),
        
        # Tests with different orders
        ("винний, зобовязаний", "зобовязаний, винний", True),
        ("зобовязаний, винний", "винний, зобовязаний", True),
        
        # Tests with additional variants
        ("зобовязаний, винний, ще якись", "зобовязаний, винний", False),
        ("зобовязаний, винний, ще якись", "ще якись, зобовязаний, винний", True),
        
        # Tests with empty strings
        ("", "", True),
        ("", "зобовязаний", False),
        
        # Tests with parenthesis
        ("грубий (про стан якоїсь речі)", "Грубий", True),
        ("грубий (про стан якоїсь речі)", "Грубий (про стан якоїсь речі)", True),
        
        # Edge cases with special characters
        ("зобовязаний!", "зобовязаний", True),
        ("винний...", "винний", False),
        
        # Tests with incorrect matches
        ("зобовязаний", "винний", False),
        ("винний", "зобовязаний", False),
        
        # Tests with numeric values
        ("123", "123", True),
        ("123", "124", False),
    )
)
def test_answer_checker(suggested: str, correct: str, result: bool):
    assert QuizAnswerChecker(suggested, correct).is_match() == result


@pytest.mark.parametrize(
    "text, to_compare, result",
    [
        ("зобовязаний, винний", "зобовязаний", True),
        ("зобовязаний, винний", "винний", True),
        ("зобовязаний, винний", "ще якись", False),
        ("грубий (про стан якоїсь речі), зобовязаний", "грубий", True),
        ("грубий (про стан якоїсь речі), зобовязаний", "зобовязаний", True),
        ("грубий (про стан якоїсь речі), зобовязаний", "про стан якоїсь речі", False),
        ("грубий (про стан якоїсь речі), зобовязаний", "грубий", True),
        ("", "зобовязаний", False),
        ("зобовязаний", "", False),
    ]
)
def test_contains(text: str, to_compare: str, result: bool):
    checker = TranslationChecker(text)
    assert (to_compare in checker) == result