import requests


class BotWebhookService:
    # TODO: make the last /bot/ prefix available to be set dynamically
    set_wh_url_pattern = "https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bot/"

    @classmethod
    def set_webhook(cls, bot_token: str, webhook_url: str):
        # TODO: use async request instead
        response = requests.post(cls.set_wh_url_pattern.format(
            bot_token=bot_token,
            webhook_url=webhook_url,
        ))

        return response.json()