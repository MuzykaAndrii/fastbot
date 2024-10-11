from app.shared.schemas import NotificationSchema


vocabulary_already_active = "Notifications for this vocabulary already active 😉"
active_vocabulary = "✅ Alerts active for: <b>{vocabulary_name}</b>"
no_active_vocabulary = "📵 Alerts is turned off"

_notification_text = "<b>{word}</b> - {translation}"
_secondary_language_pair = "<span class='tg-spoiler'><i>{word}</i> - {translation}</span>"
_sentence_example_text = "📖 {sentence}"

def get_language_pair_notification(notification_data: NotificationSchema) -> str:
    notification = _notification_text.format(
        word=notification_data.primary_lp.word,
        translation=notification_data.primary_lp.translation
    )

    if notification_data.sentence_example:
        sentence_example = _sentence_example_text.format(sentence=notification_data.sentence_example)
        notification = f"{notification}\n{sentence_example}"

        if notification_data.secondary_lp:
            secondary_lp_text = _secondary_language_pair.format(
                word=notification_data.secondary_lp.word,
                translation=notification_data.secondary_lp.translation,
            )
            notification = f"{notification}\n\n{secondary_lp_text}"
    
    return notification