from app.shared.schemas import VocabularySchema


_notification_active = " "*20 + "alerts is on ✅"
_notification_inactive = " "*19 + "alerts is off 📴"
_vocabulary_entity_header = "📃 <i>{vocabulary_name}</i>{notification_status}\n"
_vocabulary_entity_item = "{number}. <b>{word}</b> - {translation}"


def get_full_vocabulary_entity_msg(vocabulary: VocabularySchema) -> str:
    full_msg: list[str] = []
    if vocabulary.is_active:
        notification_status = _notification_active
    else:
        notification_status = _notification_inactive

    header = _vocabulary_entity_header.format(vocabulary_name=vocabulary.name, notification_status=notification_status)

    full_msg.append(header)

    for index, lang_pair in enumerate(vocabulary.language_pairs, start=1):
        full_msg.append(_vocabulary_entity_item.format(
            number=index,
            word=lang_pair.word,
            translation=lang_pair.translation,
        ))
    
    return "\n".join(full_msg)