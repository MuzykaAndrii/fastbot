from aiogram import types


from . import messages
from app.backend.components import text_generator  # simulating call to external api
from app.backend.components import vocabularies_service


async def gen_text_from_vocabulary(message: types.Message, user_id: int, vocabulary_id: int):
    vocabulary = await vocabularies_service.get_vocabulary(user_id, vocabulary_id)
    text = await text_generator.get_text_from_keywords([lang_pair.word for lang_pair in vocabulary.language_pairs])

    if text:
        response_msg = messages.generated_text.format(vocabulary_name=vocabulary.name, text=text)
    else:
        response_msg = messages.text_generator_not_available
    
    await message.answer(response_msg)