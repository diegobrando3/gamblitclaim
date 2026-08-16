"""Promo kodunun okunup yazılmasını yönetir."""
import os
from config import CODE_FILE


def get_current_code() -> str:
    """current_code.txt içindeki kodu döndürür. Dosya yoksa/boşsa hata verir."""
    if not os.path.exists(CODE_FILE):
        raise FileNotFoundError(
            f"{CODE_FILE} bulunamadı. Önce set_current_code() ile bir kod kaydet."
        )
    with open(CODE_FILE, "r", encoding="utf-8") as f:
        code = f.read().strip()
    if not code:
        raise ValueError(f"{CODE_FILE} boş, geçerli bir kod içermiyor.")
    return code


def set_current_code(code: str) -> None:
    """Kullanılacak kodu dosyaya yazar."""
    with open(CODE_FILE, "w", encoding="utf-8") as f:
        f.write(code.strip())
