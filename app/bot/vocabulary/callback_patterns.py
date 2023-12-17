from enum import Enum

from aiogram.filters.callback_data import CallbackData


class VocabularyAction(str, Enum):
    move_forward = "forward"
    move_backward = "backward"
    quiz = "quiz"
    delete = "delete"
    enable_notification = "notification_on"
    disable_notification = "notification_off"


class VocabularyCallbackData(CallbackData, prefix="vocabulary_action"):
    action: VocabularyAction
    vocabulary_id: int


class QuizStrategy(str, Enum):
    guess_native = "guess_own"
    guess_foreign = "guess_foreign"
    combined = "combined"


class StartQuizCallbackData(CallbackData, prefix="select_quiz"):
    quiz_strategy: QuizStrategy
    vocabulary_id: int