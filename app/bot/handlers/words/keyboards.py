from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_select_strategy_keyboard():
    btn_bulk = KeyboardButton(text="Bulk")
    btn_line_by_line = KeyboardButton(text="Line by line")

    select_strategy_keyboard = ReplyKeyboardMarkup(keyboard=[[
        btn_bulk,
        btn_line_by_line,
    ]])

    return select_strategy_keyboard