import requests

from app.config import settings


class MessageService:
    _send_msg_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    @classmethod
    def send_message(cls, to: int, text: str):
        requests.post(cls._send_msg_url, data={"chat_id": to, "text": text})
        