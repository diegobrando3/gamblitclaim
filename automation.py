"""
pyautogui + pytesseract ile promo kodu kullanma otomasyonu.

Ön koşul: Hedef site tarayıcıda zaten açık ve login olmuş halde
ekranda görünür olmalı.
"""
import logging
import time

import pyautogui
import pyperclip
import pytesseract

from config import (
    SITE_NAV_STEP_1,
    SITE_NAV_STEP_2,
    INPUT_BOX,
    SUBMIT_BUTTON,
    RESULT_REGION,
    OCR_LANG,
    RESULT_WAIT_SECONDS,
    NAV_STEP_WAIT_SECONDS,
)

logger = logging.getLogger(__name__)

# pyautogui güvenlik freni: fareyi ekranın sol üst köşesine götürürsen
# script anında durur (bir şey ters giderse elle müdahale imkanı)
pyautogui.FAILSAFE = True


class RedeemError(Exception):
    """Kod kullanma işlemi sırasında oluşan hatalar için."""


def _read_region(region: tuple[int, int, int, int]) -> str:
    left, top, right, bottom = region
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    text = pytesseract.image_to_string(screenshot, lang=OCR_LANG)
    return text.strip()


def _navigate_to_redeem_page() -> None:
    """Ana sayfadan redeem sayfasına giden ara adımları uygular."""
    logger.info("Redeem sayfasına gidiliyor (adım 1)...")
    pyautogui.click(SITE_NAV_STEP_1)
    time.sleep(NAV_STEP_WAIT_SECONDS)

    logger.info("Redeem sayfasına gidiliyor (adım 2)...")
    pyautogui.click(SITE_NAV_STEP_2)
    time.sleep(NAV_STEP_WAIT_SECONDS)


def redeem_code(code: str) -> str:
    """
    Kodu (panoda zaten kopyalı olduğu varsayılarak) siteye girer, gönderir
    ve sonuç mesajını OCR ile okuyup döndürür.
    """
    if INPUT_BOX == (0, 0) or SUBMIT_BUTTON == (0, 0) or RESULT_REGION == (0, 0, 0, 0):
        raise RedeemError("Koordinatlar config.py'de ayarlanmamış.")

    _navigate_to_redeem_page()

    logger.info(f"Kod giriliyor: {code}")
    pyautogui.click(INPUT_BOX)
    time.sleep(0.4)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    # Kod zaten discord_screen_reader tarafından panoya kopyalanmış durumda
    pyperclip.copy(code)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)

    pyautogui.click(SUBMIT_BUTTON)
    time.sleep(RESULT_WAIT_SECONDS)

    result_text = _read_region(RESULT_REGION)
    if not result_text:
        raise RedeemError("Sonuç bölgesinden metin okunamadı (OCR boş döndü).")

    logger.info(f"OCR sonucu: {result_text}")
    return result_text
