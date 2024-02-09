from enum import Enum

from aiogram.filters.callback_data import CallbackData


class QuizStrategy(str, Enum):
    guess_native = "guess_own"
    guess_foreign = "guess_foreign"
    combined = "combined"


class VocabularyQuizCallbackData(CallbackData, prefix="select_quiz"):
    quiz_strategy: QuizStrategy
    vocabulary_id: int