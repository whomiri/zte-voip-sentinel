import time
import threading
import datetime
from playwright.sync_api import sync_playwright

MODEM_IP = "http://192.168.1.1"
MODEM_KULLANICI = "admin"
MODEM_SIFRE = "admin"

tum_cagrilar = []
veri_kilidi = threading.Lock()

def sonuc_coz(raw_val):
    val = raw_val.strip()
    eslesmeler = {
        "0": "Bilinmeyen",
        "1": "Gelen Arama/Meşgul",
        "2": "Gelen Arama/Cevaplandı",
        "3": "Giden Arama/Cevaplanmadı",
        "4": "Giden Arama/Cevaplandı"
    }
    return eslesmeler.get(val, val)

def donus_yapilmayan_mesgulleri_bul():
    with veri_kilidi:
        if not tum_cagrilar:
            print("\n[!] Henüz arama kaydı çekilemedi veya liste boş.")
            return

        print("\n" + "=" * 55)
        print("🔍 GERİ DÖNÜŞ YAPILMAYAN (MEŞGUL/CEVAPSIZ) ÇAĞRILAR")
        print("=" * 55)

        mesgul_numaralar = {}

        for arama in tum_cagrilar:
            numara = arama["numara"]
            durum = arama["durum"]
            zaman = arama["zaman"]

            if numara in mesgul_numaralar and mesgul_numaralar[numara] == "COZULDU":
                continue

            if "Cevaplandı" in durum:
                mesgul_numaralar[numara] = "COZULDU"
            elif durum == "Gelen Arama/Meşgul":
                if numara not in mesgul_numaralar:
                    mesgul_numaralar[numara] = zaman

        bulunan = 0
        for num, zm in mesgul_numaralar.items():
            if zm != "COZULDU":
                bulunan += 1
                print(f" {bulunan}. Numara: {num} | Çağrı Zamanı: {zm} | Durum: Geri Dönüş Yapılmadı!")

        if bulunan == 0:
            print("Cevapsız/meşgul kalıp geri aranmayan hiçbir numara yok.")
        print("=" * 55 + "\n")

def donus_yapilmayanlari_kaydet():
    with veri_kilidi:
        if not tum_cagrilar:
            print("\n[!] Liste boş.")
            return

        mesgul_numaralar = {}

        for arama in tum_cagrilar:
            numara = arama["numara"]
            durum = arama["durum"]
            zaman = arama["zaman"]

            if numara in mesgul_numaralar and mesgul_numaralar[numara] == "COZULDU":
                continue

            if "Cevaplandı" in durum:
                mesgul_numaralar[numara] = "COZULDU"
            elif durum == "Gelen Arama/Meşgul":
                if numara not in mesgul_numaralar:
                    mesgul_numaralar[numara] = zaman

        bekleyenler = [(num, zm) for num, zm in mesgul_numaralar.items() if zm != "COZULDU"]

        if not bekleyenler:
            print("\n[i] Kaydedilecek geri dönülmeyen numara bulunamadı.")
            return

        bugun = datetime.datetime.now().strftime("%Y-%m-%d")
        dosya_adi = f"geri_donulmeyenler_{bugun}.txt"

        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(f"GERİ DÖNÜŞ YAPILMAYAN ARAMALAR RAPORU ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write("=" * 65 + "\n\n")
            for idx, (num, zm) in enumerate(bekleyenler, start=1):
                f.write(f"{idx}. Numara: {num} | Çağrı Zamanı: {zm} | Durum: Geri Dönüş Yapılmadı\n")

        print(f"\n[+] {len(bekleyenler)} adet numara '{dosya_adi}' dosyasına başarıyla kaydedildi.\n")

def terminal_dinleyici():
    while True:
        try:
            komut = input().strip()
            if komut == "1":
                donus_yapilmayan_mesgulleri_bul()
            elif komut == "2":
                donus_yapilmayanlari_kaydet()
        except EOFError:
            break

def run():
    global tum_cagrilar

    t = threading.Thread(target=terminal_dinleyici, daemon=True)
    t.start()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("[*] Telefona bağlanılıyor...")
        page.goto(MODEM_IP)
        page.wait_for_load_state("domcontentloaded")

        page.locator('input[type="text"]:visible').first.fill(MODEM_KULLANICI)
        sifre = page.locator('input[type="password"]:visible').first
        sifre.fill(MODEM_SIFRE)
        sifre.press("Enter")

        page.wait_for_load_state("networkidle")
        time.sleep(2)
        print("[+] Accessus concessus")

        page.evaluate("""
            if (typeof openLink === 'function') {
                openLink('voipStatus&Menu3Location=0');
            } else {
                var el = document.getElementById('voip');
                if (el) el.click();
            }
        """)
        time.sleep(2)

        print("[+] 1. True")
        log_bar = page.locator('#VOIPCallLogBar')
        log_bar.scroll_into_view_if_needed()
        log_bar.click()
        time.sleep(2)

        onceki_son_3 = []
        print("[*] 2. True")
        print("[*] Geri dönülmeyen numaraları görmek için 1, TXT kaydetmek için 2.\n")

        while True:
            try:
                satir_sayisi = page.locator("[id^='RmtNumber:']").count()
                anlik_cagrilar = []

                for i in range(satir_sayisi):
                    num_el = page.locator(f"[id='RmtNumber:{i}']")
                    sure_el = page.locator(f"[id='Duration:{i}'], [id='DurationTime:{i}']")
                    durum_el = page.locator(f"[id='Result:{i}']")
                    
                    satir = num_el.locator("xpath=..")
                    w130_el = satir.locator(".w130")
                    zaman = w130_el.first.inner_text().strip() if w130_el.count() > 0 else "-"

                    numara = num_el.inner_text().strip() if num_el.count() > 0 else ""
                    sure = sure_el.inner_text().strip() if sure_el.count() > 0 else "0"
                    durum_ham = durum_el.inner_text().strip() if durum_el.count() > 0 else ""

                    if numara:
                        anlik_cagrilar.append({
                            "numara": numara,
                            "sure": sure,
                            "durum": sonuc_coz(durum_ham),
                            "zaman": zaman
                        })

                with veri_kilidi:
                    tum_cagrilar = anlik_cagrilar

                son_3 = anlik_cagrilar[:3]
                if son_3 and son_3 != onceki_son_3:
                    onceki_son_3 = son_3
                    print(f"========== SON 3 ARAMA [{time.strftime('%H:%M:%S')}] ==========")
                    for idx, c in enumerate(son_3, start=1):
                        print(f" {idx}. Numara: {c['numara']} | Süre: {c['sure']} sn | Durum: {c['durum']} | Zaman: {c['zaman']}")
                    print("=" * 65 + "\n")

            except Exception as e:
                print(f"[!] Hata: {e}")

            time.sleep(3)

if __name__ == "__main__":
    run()
