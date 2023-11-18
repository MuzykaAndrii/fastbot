from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_select_strategy_keyboard():
    btn_bulk = KeyboardButton(text="Bulk 📝")
    btn_line_by_line = KeyboardButton(text="Line by line 🏷️")
    btn_cancel = KeyboardButton(text="Cancel")

    select_strategy_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btn_bulk, btn_line_by_line],
            [btn_cancel],
        ],
        resize_keyboard=True,
    )

    return select_strategy_keyboard