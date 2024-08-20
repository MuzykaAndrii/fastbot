from unittest.mock import Mock, AsyncMock

import pytest
from aiogram.fsm.context import FSMContext

from app.bot.modules.base_quiz.base_quiz import QuestionItem, QuestionManager, Quiz
from app.bot.modules.base_quiz.exceptions import QuestionsIsEmptyError, QuestionsIsGoneError, QuizItemNotLoadedError


def test_load_multiple_quiz_items(quiz: Quiz, question_items: list[QuestionItem]) -> None:
    for item in question_items:
        quiz.load_next_quiz_item()
        assert quiz.current_question == item.question
        assert quiz.current_answer == item.answer

    with pytest.raises(QuestionsIsGoneError):
        quiz.load_next_quiz_item()


def test_quiz_initialization(mock_question_manager: QuestionManager, mock_message: Mock) -> None:
    quiz = Quiz(
        question_manager=mock_question_manager,
        last_question_msg=mock_message,
        current_question="What is 2 + 2?",
        current_answer="4",
        correct_answers_count=2,
        wrong_answers_count=1,
        skipped_answers_count=1,
    )
    assert quiz.question_manager == mock_question_manager
    assert quiz.last_question_msg == mock_message
    assert quiz.current_question == "What is 2 + 2?"
    assert quiz.current_answer == "4"
    assert quiz.correct_answers_count == 2
    assert quiz.wrong_answers_count == 1
    assert quiz.skipped_answers_count == 1


def test_current_question_not_loaded_error(quiz: Quiz) -> None:
    with pytest.raises(QuizItemNotLoadedError):
        _ = quiz.current_question


def test_current_answer_not_loaded_error(quiz: Quiz) -> None:
    with pytest.raises(QuizItemNotLoadedError):
        _ = quiz.current_answer


def test_increment_correct_answers_count(quiz: Quiz) -> None:
    quiz.increment_correct_answers_count()
    assert quiz.correct_answers_count == 1


def test_increment_wrong_answers_count(quiz: Quiz) -> None:
    quiz.increment_wrong_answers_count()
    assert quiz.wrong_answers_count == 1


def test_increment_skipped_answers_count(quiz: Quiz) -> None:
    quiz.increment_skipped_answers_count()
    assert quiz.skipped_answers_count == 1


def test_answered_questions_count(quiz: Quiz) -> None:
    quiz.increment_correct_answers_count()
    quiz.increment_wrong_answers_count()
    quiz.increment_skipped_answers_count()

    assert quiz.answered_questions_count == 4  # Includes the initial state + 3 increments


def test_success_rate(quiz: Quiz, mock_question_manager: QuestionManager) -> None:
    quiz.correct_answers_count = 2
    assert quiz.success_rate == 66.7


def test_success_rate_zero_division_error(quiz: Quiz, mock_question_manager: QuestionManager) -> None:
    mock_question_manager.questions_count = 0

    with pytest.raises(QuestionsIsEmptyError):
        _ = quiz.success_rate


async def test_load_form_state() -> None:
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data.return_value = {
        "question_manager": Mock(spec=QuestionManager),
        "last_question_msg": None,
        "current_question": "What is 2 + 2?",
        "current_answer": "4",
        "correct_answers_count": 2,
        "wrong_answers_count": 1,
        "skipped_answers_count": 1,
    }

    quiz = await Quiz.load_form_state(mock_state)

    assert quiz.current_question == "What is 2 + 2?"
    assert quiz.current_answer == "4"
    assert quiz.correct_answers_count == 2
    assert quiz.wrong_answers_count == 1
    assert quiz.skipped_answers_count == 1


def test_quiz_dump(quiz: Quiz, mock_question_manager: QuestionManager) -> None:
    quiz._current_question = "What is 2 + 2?"
    quiz._current_answer = "4"
    quiz.correct_answers_count = 2
    quiz.wrong_answers_count = 1
    quiz.skipped_answers_count = 1

    dumped_data = quiz.dump()

    assert dumped_data["question_manager"] == mock_question_manager
    assert dumped_data["current_question"] == "What is 2 + 2?"
    assert dumped_data["current_answer"] == "4"
    assert dumped_data["correct_answers_count"] == 2
    assert dumped_data["wrong_answers_count"] == 1
    assert dumped_data["skipped_answers_count"] == 1


async def test_save_to_state(quiz: Quiz) -> None:
    mock_state = AsyncMock(spec=FSMContext)
    await quiz.save_to_state(mock_state)

    mock_state.update_data.assert_called_once_with(**quiz.dump())
