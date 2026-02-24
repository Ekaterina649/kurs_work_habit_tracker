import requests
from config import settings


def telegram_sendMessage(text, chat_id):
    params = {
        "text": text,
        "chat_id": chat_id,
    }

    requests.get(
        f"{settings.api_url}{settings.TELEGRAM_ACCESS_TOKEN}/sendMessage",
        params=params,
    )
