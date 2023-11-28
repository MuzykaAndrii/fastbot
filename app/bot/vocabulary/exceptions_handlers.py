from aiogram import F, types, Router
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent

from app.bot.vocabulary.messages import VocabularyMessages
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist


errors_handler_router = Router()

@errors_handler_router.error(ExceptionTypeFilter(VocabularyDoesNotExist), F.update.callback_query.as_("query"))
async def handle_callback_error_vocabulary_not_exist(event: ErrorEvent, query: types.CallbackQuery):
    await query.answer(text=VocabularyMessages.vocabulary_dont_exists)


@errors_handler_router.error(ExceptionTypeFilter(UserIsNotOwnerOfVocabulary), F.update.callback_query.as_("query"))
async def handle_callback_error_user_is_not_owner_of_vocabulary(event: ErrorEvent, query: types.CallbackQuery):
    await query.answer(text=VocabularyMessages.user_is_not_owner_of_vocabulary)
