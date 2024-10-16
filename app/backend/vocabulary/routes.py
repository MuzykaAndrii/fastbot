import logging

import asyncio
from fastapi import APIRouter, HTTPException, Depends

from app.backend.auth.dependencies import api_key_auth
from app.backend.vocabulary.exceptions import NoActiveVocabulariesError
from app.backend.components import notification_service
from app.bot.vocabulary.notifications import tasks  # emulation of api request to bot service


log = logging.getLogger("backend.vocabulary.routes")
router = APIRouter()


@router.post("/send_notifications", status_code=200)
async def send_notifications(auth = Depends(api_key_auth)):
    try:
        notifications = await notification_service.get_notifications()
    except NoActiveVocabulariesError:
        log.info("No active vocabularies found, skipping notifications sending")
        raise HTTPException(204, detail="No active vocabularies")

    await tasks.send_notifications(notifications)
    
    return {"detail": "success"}