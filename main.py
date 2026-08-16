"""
Günlük çalıştırılacak ana script.
Akış: Discord'da sunucuya/kanala git -> seviyene ait kod satırına çift
      tıklayıp kopyala -> current_code.txt'ye yaz -> siteye git -> kodu
      yapıştır, gönder -> sonucu OCR ile oku -> Discord'a (webhook ile) bildir.

Not: Discord masaüstü uygulaması ve hedef site sekmesi/penceresi script
çalışmadan önce açık ve login olmuş halde ekranda olmalı.

Örnek cron satırı (mesaj ~07:00'da atıldığı için biraz sonrasına kuruldu):
5 7 * * * DISPLAY=:0 XAUTHORITY=/run/user/1000/gdm/Xauthority /home/enes/promo-bot/.venv/bin/python3 /home/enes/promo-bot/main.py >> /home/enes/promo-bot/logs/redeem.log 2>&1
"""
import logging
import os
import sys

from config import FORCE_DISPLAY, FORCE_XAUTHORITY
from code_store import set_current_code
from discord_screen_reader import copy_todays_code, DiscordReadError
from automation import redeem_code, RedeemError
from notifier import notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def _ensure_display_env() -> None:
    """config.py'de FORCE_DISPLAY/FORCE_XAUTHORITY doluysa environment'a yazar."""
    if FORCE_DISPLAY:
        os.environ["DISPLAY"] = FORCE_DISPLAY
    if FORCE_XAUTHORITY:
        os.environ["XAUTHORITY"] = FORCE_XAUTHORITY

    if "DISPLAY" not in os.environ:
        logger.error("DISPLAY tanımlı değil. Script X11 oturumuna erişemez.")
        sys.exit(1)


def main() -> None:
    _ensure_display_env()

    # 1. Discord'dan kodu kopyala
    try:
        code = copy_todays_code()
        set_current_code(code)
    except DiscordReadError as e:
        logger.error(f"Discord'dan kod alınamadı: {e}")
        notify(f"⚠️ Discord'dan kod alınamadı: {e}")
        sys.exit(1)

    # 2. Siteye gir
    try:
        result = redeem_code(code)
        logger.info(f"Başarılı: {result}")
        notify(f"✅ Kod kullanıldı: `{code}`\nSonuç: {result}")
    except RedeemError as e:
        logger.error(f"Redeem hatası: {e}")
        notify(f"❌ Kod kullanılamadı: `{code}`\nHata: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Beklenmeyen hata")
        notify(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
