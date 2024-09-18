import asyncio
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

from app.backend.auth.dependencies import api_key_auth
from app.backend.text_generator.text_generator import generate_sentence_from_word
from app.backend.vocabulary.exceptions import NoActiveVocabulariesError
from app.backend.components import vocabularies_service
from app.bot.vocabulary.notifications import tasks  # emulation of api request to bot service


router = APIRouter()

@router.post("/send_notifications", status_code=200)
async def send_notifications(auth = Depends(api_key_auth)):
    try:
        lang_pairs_to_send = await vocabularies_service().get_random_lang_pair_from_every_active_vocabulary()
    except NoActiveVocabulariesError:
        # log this
        raise HTTPException(204, detail="No active vocabularies")
    
    calls = [generate_sentence_from_word(lang_pair.word) for lang_pair in lang_pairs_to_send]
    sentences = await asyncio.gather(*calls)

    for sentence, lp in zip(sentences, lang_pairs_to_send):
        lp.sentence_example = sentence

    await tasks.send_notifications(lang_pairs_to_send)
    
    return {"detail": "success"}