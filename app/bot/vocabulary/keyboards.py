from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.bot.vocabulary.callback_patterns import VocabularyAction, VocabularyCallbackButtonData


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


def get_vocabulary_actions_keyboard(vocabulary_id: int):
    delete_btn_callback_data = VocabularyCallbackButtonData(
        action=VocabularyAction.delete,
        vocabulary_id=vocabulary_id,
    )
    btn_delete = InlineKeyboardButton(
        text="❌ Delete",
        callback_data=delete_btn_callback_data.model_dump_json()
    )

    set_notification_btn_callback_data = VocabularyCallbackButtonData(
        action=VocabularyAction.set_notification,
        vocabulary_id=vocabulary_id,
    )
    btn_set_notification = InlineKeyboardButton(
        text="🕝 Set notification",
        callback_data=set_notification_btn_callback_data.model_dump_json(),
    )

    vocabulary_action_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [btn_delete, btn_set_notification],
    ])

    return vocabulary_action_keyboard