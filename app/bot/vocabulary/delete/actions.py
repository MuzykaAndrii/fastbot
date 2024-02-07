from aiogram.types import CallbackQuery

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.show.actions import show_vocabulary
from . import messages
from app.shared.exceptions import NoVocabulariesFound
from app.vocabulary.services import VocabularyService


async def delete_vocabulary(
    from_user: int,
    target_vocabulary_id: int,
    query: CallbackQuery,
):
    await VocabularyService.delete_vocabulary(from_user, target_vocabulary_id)

    try:
        latest_vocabulary = await VocabularyService.get_recent_user_vocabulary(from_user)
    
    except NoVocabulariesFound:
        await query.message.edit_text(VocabularyMessages.user_havent_any_vocabularies)
        await query.message.edit_reply_markup(reply_markup=None)

    else:
        await show_vocabulary(latest_vocabulary, edit_existing=query.message)

    finally:
        await query.answer(text=messages.vocabulary_deleted_successfully)