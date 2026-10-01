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
   git clone [https://github.com/whomiri/zte-voip-sentinel.git](https://github.com/whomiri/zte-voip-sentinel.git)
   cd zte-voip-sentinel
   ```

2. **Gerekli bağımlılıkları yükleyin:**
   ```bash
   pip install playwright
   playwright install chromium
   ```

3. **Yapılandırma:**
   `main.py` içindeki modem erişim bilgilerini kendi ağınıza göre düzenleyin:
   ```python
   MODEM_IP = "[http://192.168.1.1](http://192.168.1.1)"
   MODEM_KULLANICI = "admin"
   MODEM_SIFRE = "admin"
   ```

---

## 💻 Kullanım

Scripti başlatın:
```bash
python main.py
```

Program çalışırken terminal arka planda komut dinlemeye devam eder:

| Tuş | Eylem |
|---|---|
| `1` | Geri dönüş yapılmamış meşgul/cevapsız çağrıları ekranda listeler. |
| `2` | Henüz çözülmemiş numaraları `geri_donulmeyenler_YYYY-MM-DD.txt` dosyasına kaydeder. |

---

## 🖥️ Örnek Çıktı

```text
[*] Telefona bağlanılıyor...
[+] Accessus concessus
[+] 1. True
[*] 2. True
[*] Geri dönülmeyen numaraları görmek için 1, TXT kaydetmek için 2.

========== SON 3 ARAMA ==========
 1. Numara: 0532XXXXXXX | Süre: 48 sn | Durum: Gelen Arama/Cevaplandı | Zaman: 2026-10-01 12:34:02
 2. Numara: 0541XXXXXXX | Süre: 0 sn | Durum: Gelen Arama/Meşgul | Zaman: 2026-10-01 12:30:15
 3. Numara: 0505XXXXXXX | Süre: 120 sn | Durum: Giden Arama/Cevaplandı | Zaman: 2026-10-01 12:15:40
=================================================================
```

`1` tuşuna basıldığında:
```text
=======================================================
🔍 GERİ DÖNÜŞ YAPILMAYAN (MEŞGUL/CEVAPSIZ) ÇAĞRILAR
=======================================================
 1. Numara: 0541XXXXXXX | Çağrı Zamanı: 2026-10-01 12:30:15 | Durum: Geri Dönüş Yapılmadı!
=======================================================
```

---

## 🔒 Güvenlik Notu

Depoya commit atmadan önce `main.py` dosyasında gerçek modem şifrenizin yer almadığından emin olun. Şifreyi çevre değişkeni (`os.getenv`) veya yerel `.env` dosyası üzerinden okumak en güvenli yaklaşımdır.

---

## 📄 Lisans

Bu proje [MIT](LICENSE) lisansı ile lisanslanmıştır.
