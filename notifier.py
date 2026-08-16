"""Discord webhook üzerinden bildirim gönderir."""
import logging
import requests
from config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)


def notify(message: str) -> bool:
    """Discord kanalına mesaj gönderir. Başarılıysa True döner."""
    if not DISCORD_WEBHOOK_URL:
        logger.warning("DISCORD_WEBHOOK_URL tanımlı değil, bildirim atlanıyor.")
        return False
    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Webhook gönderilemedi: {e}")
        return False
