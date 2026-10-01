# 📡 zte-voip-sentinel

> Real-time VoIP call log monitor and smart missed-call tracker for **ZTE ZXHN H3600P** routers via Python & Playwright.

`zte-voip-sentinel`, ZTE H3600P modemlerin web yönetim arayüzüne arka planda bağlanarak VoIP çağrı kayıtlarını canlı izleyen, meşgule düşen veya yanıtsız kalan çağrıları sonradan yapılan geri dönüşlerle eşleştiren ve çözülmemiş cevapsız aramaları tek tuşla listeleyen/dışa aktaran bir CLI otomasyon aracıdır.

---

## ⚡ Özellikler

- **Headless Tarayıcı Otomasyonu:** Playwright ile Chromium motorunu tamamen arka planda çalıştırır, arayüzü kasmadan `#VOIPCallLogBar` tablosunu anlık parse eder.
- **Canlı Çağrı Akışı:** Hatta düşen son 3 çağrıyı (Numara, Süre, Durum, Zaman) konsola anlık yazdırır.
- **Akıllı Geri Arama Korelasyonu:**
  - `Gelen Arama/Meşgul` olan numaraları takip listesine alır.
  - Aynı numara daha sonra tekrar arayıp bağlandığında veya ofisten geri aranıp konuşulduğunda (`Cevaplandı`), sistem durumu otomatik olarak **"ÇÖZÜLDÜ"** işaretler ve listeden düşürür.
- **Asenkron Terminal Dinleyici:** Kazıma döngüsünü kesintiye uğratmadan çalışan çoklu iş parçacığı (multi-threading):
  - `1` + Enter: Geri aranmayan meşgul çağrıları terminale döker.
  - `2` + Enter: Bekleyen aramaları tarih damgalı `.txt` raporu olarak kaydeder.

---

## 🛠️ Kurulum

1. **Depoyu klonlayın:**
   ```bash
   git clone [https://github.com/kullanici_adiniz/zte-voip-sentinel.git](https://github.com/kullanici_adiniz/zte-voip-sentinel.git)
   cd zte-voip-sentinel
