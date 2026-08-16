"""
Merkezi ayar dosyası. Hassas bilgiler (.env) üzerinden okunur,
koordinatlar coord_finder aracı (screenshot üzerinde tıklama) ile bulundu.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Discord: bildirim gönderme (webhook) ---
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# --- X11 / ekran erişimi (laptop üzerinde çalıştırılırken gerekli) ---
FORCE_DISPLAY = os.getenv("FORCE_DISPLAY", "")       # örn: ":0"
FORCE_XAUTHORITY = os.getenv("FORCE_XAUTHORITY", "")  # örn: "/run/user/1000/gdm/Xauthority"

# --- Discord ekran koordinatları ---
DISCORD_SERVER_ICON = (751, 139)
DISCORD_CHANNEL_POSITION = (890, 380)
# Kendi seviyene ait kod satırının pozisyonu (çift tıklanıp kopyalanır)
CODE_TEXT_POSITION = (1264, 179)

# --- Site: redeem sayfasına gitmek için ara adımlar ---
SITE_NAV_STEP_1 = (581, 143)
SITE_NAV_STEP_2 = (576, 433)

# --- Site: kod girme ---
INPUT_BOX = (384, 461)
SUBMIT_BUTTON = (386, 508)

# --- Site: sonuç mesajının okunacağı bölge (left, top, right, bottom) ---
RESULT_REGION = (386, 674, 677, 717)

# --- OCR ---
OCR_LANG = "tur"

# --- Zamanlama davranışı ---
RESULT_WAIT_SECONDS = 2.5
NAV_STEP_WAIT_SECONDS = 1.0
