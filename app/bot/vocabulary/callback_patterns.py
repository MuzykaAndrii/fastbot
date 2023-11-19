from enum import Enum

from aiogram.filters.callback_data import CallbackData


class VocabularyAction(str, Enum):
    delete = "delete"
    set_notification = "notification"


class VocabularyCallbackData(CallbackData, prefix="vocabulary_action"):
    action: VocabularyAction
    vocabulary_id: int