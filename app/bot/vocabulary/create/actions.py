from aiogram import types

from app.bot.vocabulary.parsers import VocabularyParser
from app.shared.schemas import VocabularyCreateSchema
from app.backend.components import vocabularies_service


async def create_vocabulary(message: types.Message, vocabulary_name: str):
    language_lairs = VocabularyParser().parse_bulk_vocabulary(message.text)

    vocabulary = VocabularyCreateSchema(
        owner_id=message.from_user.id,
        name=vocabulary_name,
        language_pairs=language_lairs,
    )

    await vocabularies_service().create_vocabulary(vocabulary)
    await message.answer("Vocabulary saved successfully! 🎉 Check it out using /my command!")