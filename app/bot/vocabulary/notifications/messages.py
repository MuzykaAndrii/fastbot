from app.shared.schemas import ExtendedLanguagePairSchema


vocabulary_already_active = "Notifications for this vocabulary already active 😉"
active_vocabulary = "✅ Alerts active for: <b>{vocabulary_name}</b>"
no_active_vocabulary = "📵 Alerts is turned off"

_notification_text = "<b>{word}</b> - {translation}"
_sentence_example_text = "📖 {sentence}"

def get_language_pair_notification(lang_pair: ExtendedLanguagePairSchema) -> str:
    notification = _notification_text.format(
        word=lang_pair.word,
        translation=lang_pair.translation
    )

    if lang_pair.sentence_example:
        sentence_example = _sentence_example_text.format(sentence=lang_pair.sentence_example)
        notification = f"{notification}\n{sentence_example}"
    
    return notification