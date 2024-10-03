from aiogram.types import CallbackQuery

from app.bot.vocabulary.messages import VocabularyMessages
from app.bot.vocabulary.show.actions import show_vocabulary_in_existing_msg
from . import messages
from app.shared.exceptions import NoVocabulariesFound
from app.backend.components import vocabularies_service


async def delete_vocabulary(
    from_user: int,
    target_vocabulary_id: int,
    query: CallbackQuery,
):
    await vocabularies_service.delete_vocabulary(from_user, target_vocabulary_id)

    try:
        latest_vocabulary = await vocabularies_service.get_recent_user_vocabulary(from_user)
    
    except NoVocabulariesFound:
        await query.message.edit_text(VocabularyMessages.user_havent_any_vocabularies)
        await query.message.edit_reply_markup(reply_markup=None)

    else:
        await show_vocabulary_in_existing_msg(latest_vocabulary, query.message)

    finally:
        await query.answer(text=messages.vocabulary_deleted_successfully)