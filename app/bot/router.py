from fastapi import APIRouter, Request

from app.bot.schemas import TgBotResponse
from app.bot.services.message import MessageService


router = APIRouter(prefix="/bot", tags=['bot'])

@router.post('/')
async def test(request: Request):
    result = await request.json()
    tg_response = TgBotResponse.model_validate(result)

    msg = tg_response.message.text
    uid = tg_response.message.from_user.id

    MessageService.send_message(to=uid, text=msg)

    return ""