import requests

print("--- 💬 Hızlı SMS Gönderim Sistemi ---")

# Kullanıcıdan dinamik olarak numara ve mesaj içeriği alınıyor
hedef_numara = input("Mesaj atılacak numara (Örn: +905XXXXXXXXX): ")
mesaj_icerigi = input("Mesajınızın içeriğini yazın: ")

print("\nMesajınız iletiliyor, lütfen bekleyin...")

try:
    # API isteği gönderiliyor
    resp = requests.post('https://textbelt.com', {
        'phone': hedef_numara,
        'message': mesaj_icerigi, # Yazdığın içeriği aynen gönderir
        'key': 'textbelt',       # Kayıt gerektirmeyen ücretsiz genel anahtar
    })
    
    sonuc = resp.json()
    
    if sonuc.get('success'):
        print(f"✅ Başarılı! Mesajınız iletildi.")
        print(f"🆔 Mesaj ID: {sonuc.get('textId')}")
    else:
        print(f"❌ Hata Oluştu: {sonuc.get('error')}")

except Exception as e:
    print(f"❌ Bağlantı hatası: {e}")
