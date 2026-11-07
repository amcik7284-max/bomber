import requests

print("--- 💬 Hızlı SMS Gönderim Sistemi ---")

hedef_numara = input("Mesaj atılacak numara (Örn: +905XXXXXXXXX): ")
mesaj_icerigi = input("Mesajınızın içeriğini yazın: ")

print("\nMesajınız iletiliyor, lütfen bekleyin...")

try:
    # API isteği gönderiliyor
    resp = requests.post('https://textbelt.com', {
        'phone': hedef_numara,
        'message': mesaj_icerigi,
        'key': 'textbelt',
    })
    
    # Sunucu durum kodu kontrolü (200 başarılı demektir)
    if resp.status_code == 200:
        try:
            sonuc = resp.json()
            if sonuc.get('success'):
                print(f"✅ Başarılı! Mesajınız iletildi.")
                print(f"🆔 Mesaj ID: {sonuc.get('textId')}")
            else:
                print(f"❌ Servis Hatası: {sonuc.get('error')}")
        except ValueError:
            print("❌ Hata: Sunucu JSON formatında yanıt vermedi. Muhtemelen limit engelini aştınız.")
            print(f"Sunucudan dönen ham metin: {resp.text}")
    else:
        print(f"❌ Sunucu Hatası! Durum Kodu: {resp.status_code}")
        print("Açıklama: Ücretsiz servis isteklerinizi engelliyor olabilir.")

except Exception as e:
    print(f"❌ Bağlantı hatası: {e}")
