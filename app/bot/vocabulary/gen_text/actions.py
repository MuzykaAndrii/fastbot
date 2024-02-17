from aiogram import types


from . import messages
from app.backend.text_generator.text_generator import generate_text_from_words
from app.vocabulary.services import VocabularyService


async def gen_text_from_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    vocabulary = await VocabularyService.get_vocabulary(user_id, vocabulary_id)
    text = await generate_text_from_words(lang_pair.word for lang_pair in vocabulary.language_pairs)

    if text:
        response_msg = messages.generated_text.format(vocabulary_name=vocabulary.name, text=text)
    else:
        response_msg = messages.text_generator_not_available
    
    await message.answer(response_msg)