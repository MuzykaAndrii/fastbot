from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData
from app.bot.vocabulary.schemas import VocabularySetSchema


def get_select_strategy_keyboard():
    btn_bulk = KeyboardButton(text="Bulk")
    btn_line_by_line = KeyboardButton(text="Line by line")
    btn_cancel = KeyboardButton(text="Cancel")

    select_strategy_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btn_bulk, btn_line_by_line],
            [btn_cancel],
        ],
        resize_keyboard=True,
    )

    return select_strategy_keyboard


class ActionsKeyboard:
    def __init__(self, vocabulary: VocabularySetSchema) -> None:
        self.vocabulary = vocabulary
    
    def get_markup(self):
        if self.vocabulary.is_active:
            notification_btn = self.disable_notification_btn
        else:
            notification_btn = self.enable_notification_btn

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [self.delete_btn, self.quiz_btn],
            [notification_btn],
            [self.move_backward_btn, self.move_forward_btn],
        ])

        return keyboard

    @property
    def quiz_btn(self):
        return InlineKeyboardButton(
            text="📝 Start quiz",
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
            text="🕝 Turn on alerts",
            callback_data=self._make_callback_data(VocabularyAction.enable_notification),
        )

    @property
    def disable_notification_btn(self):
        return InlineKeyboardButton(
            text="🚫 Turn off alerts",
            callback_data=self._make_callback_data(VocabularyAction.disable_notification),
        )
    
    def _make_callback_data(self, action: VocabularyAction):
        callback_data = VocabularyCallbackData(
            action=action,
            vocabulary_id=self.vocabulary.id,
        )
        return callback_data.pack()
