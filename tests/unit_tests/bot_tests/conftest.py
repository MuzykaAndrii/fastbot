from unittest.mock import Mock

import pytest
from aiogram.types.message import Message

from app.bot.modules.base_quiz.base_quiz import QuestionItem, QuestionManager, Quiz
from app.bot.modules.base_quiz.exceptions import QuestionsIsGoneError


@pytest.fixture
def question_items() -> list[QuestionItem]:
    return [
        QuestionItem(question="What is 2 + 2?", answer="4"),
        QuestionItem(question="What is the capital of France?", answer="Paris"),
        QuestionItem(question="What is the boiling point of water?", answer="100°C"),
    ]


@pytest.fixture
def mock_question_manager(question_items: list[QuestionItem]) -> QuestionManager:
    mock_manager = Mock(spec=QuestionManager)
    mock_manager.get_question_item.side_effect = question_items + [QuestionsIsGoneError]
    mock_manager.questions_count = len(question_items)
    return mock_manager


@pytest.fixture
def mock_message() -> Mock:
    return Mock(spec=Message)


@pytest.fixture
def quiz(mock_question_manager: QuestionManager) -> Quiz:
    return Quiz(question_manager=mock_question_manager)