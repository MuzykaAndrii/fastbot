from enum import Enum

from aiogram.filters.callback_data import CallbackData


class VocabularyAction(str, Enum):
    move_forward = "forward"
    move_backward = "backward"
    quiz = "quiz"
    delete = "delete"
    enable_notification = "notification"


class VocabularyCallbackData(CallbackData, prefix="vocabulary_action"):
    action: VocabularyAction
    vocabulary_id: int