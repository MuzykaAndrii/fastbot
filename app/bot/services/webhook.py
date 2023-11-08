import requests


class BotWebhookService:
    # TODO: make the last /bot/ prefix available to be set dynamically
    _set_wh_url_pattern = "https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/"
    _unset_wh_url_pattern = "https://api.telegram.org/bot{bot_token}/deleteWebhook?drop_pending_updates=False"
    _get_wh_info_url_pattern = "https://api.telegram.org/bot{bot_token}/getWebhookInfo"

    def __init__(self, bot_token: str, webhook_url: str, webhook_prefix: str = "/") -> None:
        self.bot_token = bot_token
        self.webhook_url = webhook_url + webhook_prefix
    
    def set_webhook_if_current_unmatched(self):
        current_webhook = self.get_webhook_info()

        if current_webhook.get('url') != self.webhook_url:
            self.set_webhook()
        return

    def get_webhook_info(self) -> dict:
        response = requests.post(self._get_wh_info_url_pattern.format(
            bot_token=self.bot_token,
        ))
        return response.json()


    def set_webhook(self):
        # TODO: use async request instead
        response = requests.post(self._set_wh_url_pattern.format(
            bot_token=self.bot_token,
            webhook_url=self.webhook_url,
        ))

        return response.json()
    
    def unset_webhook(self):
        response = requests.post(self._unset_wh_url_pattern.format(
            bot_token=self.bot_token,
        ))

        return response.json()