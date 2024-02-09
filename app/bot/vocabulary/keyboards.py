from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.callback_patterns import (
    VocabularyAction,
    VocabularyCallbackData
)
from app.shared.schemas import VocabularySchema


class ActionsKeyboard:
    def __init__(self, vocabulary: VocabularySchema) -> None:
        self.vocabulary = vocabulary
    
    def get_markup(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [self.delete_btn, self.append_btn, self.notification_btn],
            [self.gen_text_btn, self.quiz_btn,],
            [self.move_backward_btn, self.move_forward_btn],
        ])

        return keyboard
    
    @property
    def append_btn(self):
        return InlineKeyboardButton(
            text="➕ Add words",
            callback_data=self._make_callback_data(VocabularyAction.append_language_pairs),
        )
    
    @property
    def gen_text_btn(self):
        return InlineKeyboardButton(
            text="📖 Story",
            callback_data=self._make_callback_data(VocabularyAction.gen_text),
        )

    @property
    def quiz_btn(self):
        return InlineKeyboardButton(
            text="📝 Quiz",
            callback_data=self._make_callback_data(VocabularyAction.quiz)
        )
    
    @property
    def move_forward_btn(self):
        return InlineKeyboardButton(
            text="Next ⏩",
            callback_data=self._make_callback_data(VocabularyAction.move_forward),
        )
    
    @property
    def move_backward_btn(self):
        return InlineKeyboardButton(
            text="⏪ Prev",
            callback_data=self._make_callback_data(VocabularyAction.move_backward),
        )
    
    @property
    def delete_btn(self):
        return InlineKeyboardButton(
            text="❌ Delete",
            callback_data=self._make_callback_data(VocabularyAction.delete),
        )
    
    @property
    def enable_notification_btn(self):
        return InlineKeyboardButton(
            text="🕝 Enable alerts",
            callback_data=self._make_callback_data(VocabularyAction.enable_notification),
        )

    @property
    def disable_notification_btn(self):
        return InlineKeyboardButton(
            text="📵 Disable alerts",
            callback_data=self._make_callback_data(VocabularyAction.disable_notification),
        )
    
    @property
    def notification_btn(self):
        if self.vocabulary.is_active:
            return self.disable_notification_btn
        else:
            return self.enable_notification_btn
    
    def _make_callback_data(self, action: VocabularyAction):
        callback_data = VocabularyCallbackData(
            action=action,
            vocabulary_id=self.vocabulary.id,
        )
        return callback_data.pack()
