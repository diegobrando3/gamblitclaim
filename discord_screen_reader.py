"""
Discord masaüstü uygulamasını pyautogui ile gezip, kullanıcının seviyesine
ait kod satırına çift tıklayarak kelimeyi seçer ve panoya kopyalar.

Ön koşul: Discord uygulaması açık ve login olmuş halde ekranda görünür
olmalı. CODE_TEXT_POSITION, mesaj içinde HER GÜN aynı satırda duran
(sadece kod içeriği değişen) senin seviyene ait satırı işaret etmeli.
"""
import logging
import time

import pyautogui
import pyperclip

from config import DISCORD_SERVER_ICON, DISCORD_CHANNEL_POSITION, CODE_TEXT_POSITION

logger = logging.getLogger(__name__)


class DiscordReadError(Exception):
    """Discord'dan kod kopyalama sırasında oluşan hatalar için."""


def copy_todays_code() -> str:
    """
    Discord'da sunucuya, kanala girip kod satırına çift tıklar,
    panoya kopyalar ve kopyalanan metni döndürür.
    """
    if (
        DISCORD_SERVER_ICON == (0, 0)
        or DISCORD_CHANNEL_POSITION == (0, 0)
        or CODE_TEXT_POSITION == (0, 0)
    ):
        raise DiscordReadError("Discord koordinatları config.py'de ayarlanmamış.")

    logger.info("Discord sunucusuna geçiliyor...")
    pyautogui.click(DISCORD_SERVER_ICON)
    time.sleep(1.0)

    logger.info("Kanala giriliyor...")
    pyautogui.click(DISCORD_CHANNEL_POSITION)
    time.sleep(1.5)  # mesajların yüklenmesini bekle

    logger.info("Kod satırına çift tıklanıyor...")
    # Panoyu önce temizle, çift tık gerçekten yeni bir şey seçti mi anlayabilelim
    pyperclip.copy("")
    pyautogui.doubleClick(CODE_TEXT_POSITION)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.3)

    code = pyperclip.paste().strip()
    if not code:
        raise DiscordReadError("Kod kopyalanamadı (pano boş döndü).")

    logger.info(f"Kopyalanan kod: {code}")
    return code
