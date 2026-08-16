"""
Site açıkken bu scripti çalıştır. 5 saniye içinde fareni istediğin
noktaya (input kutusu, submit butonu, sonuç bölgesinin köşeleri) götür,
koordinatı terminale yazdırır. Ctrl+C ile çık.

Kullanım:
    python3 coord_finder.py
"""
import time
import pyautogui

print("Fareni hedef noktaya götür. Her 2 saniyede bir konum yazdırılacak.")
print("Çıkmak için Ctrl+C.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Konum: ({x}, {y})")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nÇıkıldı.")
