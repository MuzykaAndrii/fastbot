import requests

from app.config import settings


class BotWebhookService:
    # TODO: make the last /bot/ prefix available to be set dynamically
    set_wh_url_pattern = "https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bot/"

    @classmethod
    def set_webhook(cls):
        # TODO: use async request instead
        response = requests.post(cls.set_wh_url_pattern.format(
            bot_token=settings.BOT_TOKEN,
            webhook_url=settings.WEBHOOK_URL,
        ))

        return response.json()