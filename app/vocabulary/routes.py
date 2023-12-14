from fastapi import APIRouter, HTTPException

from app.config import settings
from app.vocabulary.schemas import AuthorizationSchema
from app.vocabulary.services import VocabularyService
from app.bot.vocabulary import tasks  # emulation of api request to bot service


router = APIRouter()

@router.post("/send_notifications", status_code=200)
async def send_notifications(auth: AuthorizationSchema):
    if auth.api_key != settings.API_KEY:
        raise HTTPException(403, detail="Invalid API key")
    
    active_vocabularies = await VocabularyService.get_active_vocabularies()

    if not active_vocabularies:
        raise HTTPException(204, detail="No active vocabularies")

    await tasks.send_notifications(active_vocabularies)
    
    return {"detail": "success"}