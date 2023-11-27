from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackData


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
    def __init__(self, vocabulary) -> None:
        self.vocabulary = vocabulary
    
    def get_markup(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [self.delete_btn, self.quiz_btn],
            [self.enable_notification_btn],
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
    
    def _make_callback_data(self, action: VocabularyAction):
        callback_data = VocabularyCallbackData(
            action=action,
            vocabulary_id=self.vocabulary.id,
        )
        return callback_data.pack()


# def get_vocabulary_actions_keyboard(vocabulary_id: int):
#     quiz_btn_callback_data = VocabularyCallbackData(
#         action=VocabularyAction.quiz,
#         vocabulary_id=vocabulary_id,
#     )
#     btn_quiz = InlineKeyboardButton(
#         text="📝 Start quiz",
#         callback_data=quiz_btn_callback_data.pack(),
#     )

#     move_forward_btn_callback_data = VocabularyCallbackData(
#         action=VocabularyAction.move_forward,
#         vocabulary_id=vocabulary_id,
#     )
#     btn_move_forward = InlineKeyboardButton(
#         text="Next ⏩",
#         callback_data=move_forward_btn_callback_data.pack(),
#     )

#     move_backward_btn_callback_data = VocabularyCallbackData(
#         action=VocabularyAction.move_backward,
#         vocabulary_id=vocabulary_id,
#     )
#     btn_move_backward = InlineKeyboardButton(
#         text="⏪ Prev",
#         callback_data=move_backward_btn_callback_data.pack(),
#     )

#     delete_btn_callback_data = VocabularyCallbackData(
#         action=VocabularyAction.delete,
#         vocabulary_id=vocabulary_id,
#     )
#     btn_delete = InlineKeyboardButton(
#         text="❌ Delete",
#         callback_data=delete_btn_callback_data.pack(),
#     )

#     enable_notification_btn_callback_data = VocabularyCallbackData(
#         action=VocabularyAction.enable_notification,
#         vocabulary_id=vocabulary_id,
#     )
#     btn_enable_notification = InlineKeyboardButton(
#         text="🕝 Set notification",
#         callback_data=enable_notification_btn_callback_data.pack(),
#     )

#     vocabulary_action_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [btn_delete, btn_quiz, btn_enable_notification],
#         [btn_move_backward, btn_move_forward],
#     ])

#     return vocabulary_action_keyboard