from enum import Enum

from pydantic import BaseModel


class VocabularyAction(str, Enum):
    delete = "delete"
    set_notification = "notification"


class VocabularyCallbackButtonData(BaseModel):
    action: VocabularyAction
    vocabulary_id: int