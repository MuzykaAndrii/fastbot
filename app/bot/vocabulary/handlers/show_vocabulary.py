from aiogram.filters import Command
from aiogram import Router, types

from app.users.services.user import UserService
from app.vocabulary.dal import VocabularySetDAL


router = Router()


@router.message(Command("my"))
async def show_vocabularies(message: types.Message):
    user = await UserService.get_by_tg_id(message.from_user.id)
    if not user:
        message.answer("You're haven't any vocabularies yet(")

    vocabulary_sets = await VocabularySetDAL.filter_by(owner_id=user.id)

    for vocabulary_set in vocabulary_sets:
        msg_entities: list[str] = [f"<i>{vocabulary_set.name}</i>"]

        for index, lang_pair in enumerate(vocabulary_set.language_pairs):
            msg_entities.append(
                f"<u>{index+1}.</u> <b>{lang_pair.word}</b> - {lang_pair.translation}"
            )
        await message.answer("\n".join(msg_entities))