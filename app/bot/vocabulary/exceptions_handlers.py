from aiogram import F, types, Router
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.notifications import messages as notification_messages
from app.shared.exceptions import (
    NoVocabulariesFound,
    UserIsNotOwnerOfVocabulary,
    VocabularyDoesNotExist,
    VocabularyIsAlreadyActive,
)


errors_handler_router = Router()

@errors_handler_router.error(ExceptionTypeFilter(VocabularyDoesNotExist), F.update.callback_query.as_("query"))
async def handle_callback_error_vocabulary_not_exist(event: ErrorEvent, query: types.CallbackQuery):
    await query.answer(text=VocabularyMessages.vocabulary_dont_exists)


@errors_handler_router.error(ExceptionTypeFilter(UserIsNotOwnerOfVocabulary), F.update.callback_query.as_("query"))
async def handle_callback_error_user_is_not_owner_of_vocabulary(event: ErrorEvent, query: types.CallbackQuery):
    await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)


@errors_handler_router.error(ExceptionTypeFilter(VocabularyIsAlreadyActive), F.update.callback_query.as_("query"))
async def handle_callback_error_vocabulary_is_already_active(event: ErrorEvent, query: types.CallbackQuery):
    await query.answer(text=notification_messages.vocabulary_already_active)


@errors_handler_router.error(ExceptionTypeFilter(NoVocabulariesFound), F.update.message.as_("message"))
async def handle_message_error_no_vocabularies_found(event: ErrorEvent, message: types.Message):
    await message.answer(VocabularyMessages.user_havent_any_vocabularies)