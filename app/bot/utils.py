from aiogram.types import Message, CallbackQuery


def recognize_update(update: Message | CallbackQuery) -> Message:
    match update:
        case Message():
            return update
        case CallbackQuery():
            return update.message
        case _:
            return update