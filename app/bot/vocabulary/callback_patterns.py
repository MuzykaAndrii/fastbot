from enum import Enum

from aiogram.filters.callback_data import CallbackData


class VocabularyAction(str, Enum):
    move_forward = "forward"
    move_backward = "backward"
    quiz = "quiz"
    delete = "delete"
    enable_notification = "notification_on"
    disable_notification = "notification_off"
    gen_text = "gen_text"
    append_language_pairs = "append_language_pairs"


class VocabularyCallbackData(CallbackData, prefix="vocabulary_action"):
    action: VocabularyAction
    vocabulary_id: int
