from app.bot.vocabulary.schemas import VocabularySetSchema


class VocabularyMessages:
    user_havent_any_vocabularies = "You're haven't any vocabularies yet("
    user_is_not_owner_of_vocabulary = "☢️ You're not owner of this vocabulary! ☢️"
    vocabulary_deleted_successfully = "🗑️ Vocabulary deleted successfully 🫡"
    vocabulary_entity_header = "<i>{vocabulary_name}</i>"
    vocabulary_entity_active = " - ✅ Notifications active ✅"
    vocabulary_entity_item = "<u>{number}.</u> <b>{word}</b> - {translation}"
    
    @classmethod
    def get_vocabulary_entity_msg(cls, vocabulary_set: VocabularySetSchema) -> str:
        full_msg: list[str] = []
        header = cls.vocabulary_entity_header.format(vocabulary_name=vocabulary_set.name)

        if vocabulary_set.is_active:
            header += cls.vocabulary_entity_active

        full_msg.append(header)

        for index, lang_pair in enumerate(vocabulary_set.language_pairs, start=1):
            full_msg.append(cls.vocabulary_entity_item.format(
                number=index,
                word=lang_pair.word,
                translation=lang_pair.translation,
            ))
        
        return "\n".join(full_msg)