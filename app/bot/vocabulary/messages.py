from app.bot.vocabulary.schemas import VocabularySetSchema


class VocabularyMessages:
    user_havent_any_vocabularies = "You're haven't any vocabularies yet("
    user_is_not_owner_of_vocabulary = "☢️ You're not owner of this vocabulary! ☢️"
    vocabulary_deleted_successfully = "🗑️ Vocabulary deleted successfully 🫡"
    vocabulary_dont_exists = "Vocabulary does not exist 🤷🏻‍♂️"

    bulk_vocabulary_creation_rules = """
    <b>There are several rules to create bulk vocabulary:</b>

📝 <b>Format:</b> Enter word pairs with a hyphen "-" on each line.
🚫 <b>Minimum Pairs:</b> Include at least two pairs. Less won't cut it!
🔄 <b>Case Insensitive:</b> Cases don't matter; "Word - Translation" = "word - translation."
✨ <b>Special Characters:</b> Go ahead, use emojis, punctuation, or anything fancy!
➖ <b>Hyphen in Words:</b> Totally allowed, but only as a separator.
🌟 <b>Multiple Translations:</b> Use commas for multiple translations, like "Word - Translation, Another."
🎉 <b>Have Fun!</b> Enjoy expanding your vocabulary with the bot! 🚀
    """
    vocabulary_already_active = "Notifications for this vocabulary already active 😉"
    vocabulary_entity_header = "<i>{vocabulary_name}</i>"
    active_vocabulary = "✅ Notifications active for: <b>{vocabulary_name}</b>"
    no_active_vocabulary = "📵 Notifications is turned off"
    vocabulary_entity_item = "<u>{number}.</u> <b>{word}</b> - {translation}"
    language_pair_notification = "<b>{word}</b> - {translation}"
    
    @classmethod
    def get_vocabulary_entity_msg(cls, vocabulary_set: VocabularySetSchema) -> str:
        full_msg: list[str] = []
        header = cls.vocabulary_entity_header.format(vocabulary_name=vocabulary_set.name)

        full_msg.append(header)

        for index, lang_pair in enumerate(vocabulary_set.language_pairs, start=1):
            full_msg.append(cls.vocabulary_entity_item.format(
                number=index,
                word=lang_pair.word,
                translation=lang_pair.translation,
            ))
        
        return "\n".join(full_msg)