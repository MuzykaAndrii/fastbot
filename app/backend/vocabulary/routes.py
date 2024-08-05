from fastapi import APIRouter, HTTPException

from app.backend.components.config import auth_settings
from app.backend.text_generator.text_generator import generate_sentence_from_word
from app.shared.schemas import ExtendedLanguagePairSchema
from app.backend.vocabulary.schemas import AuthorizationSchema
from app.backend.components import vocabularies_service
from app.bot.vocabulary.notifications import tasks  # emulation of api request to bot service


router = APIRouter()

@router.post("/send_notifications", status_code=200)
async def send_notifications(auth: AuthorizationSchema):
    if auth.api_key != auth_settings.API_KEY:
        raise HTTPException(403, detail="Invalid API key")
    
    lang_pairs_to_send: list[ExtendedLanguagePairSchema] = await vocabularies_service().get_random_lang_pair_from_every_active_vocabulary()

    if not lang_pairs_to_send:
        raise HTTPException(204, detail="No active vocabularies")

    for lang_pair in lang_pairs_to_send:
        lang_pair.sentence_example = await generate_sentence_from_word(lang_pair.word)

    await tasks.send_notifications(lang_pairs_to_send)
    
    return {"detail": "success"}