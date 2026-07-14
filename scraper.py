import requests
from bs4 import BeautifulSoup
import json
import time

urls = [
    "https://gataelektrik.com/orta-gerilim-2021-fiyat",
    "https://gataelektrik.com/og-guvenlik-malzemeleri",
    "https://gataelektrik.com/og-sarf-malzemeler-2021",
    "https://gataelektrik.com/topraklama-malzemeleri-2022",
    "https://gataelektrik.com/prysmian-fiyat-listesi",
    "https://gataelektrik.com/hes-kablo-fiyat-listes",
    "https://gataelektrik.com/kablo-fiyat-listesi",
    "https://gataelektrik.com/aluminyum-kablo-2021",
    "https://gataelektrik.com/kaucuk-kablo-fiyat",
    "https://gataelektrik.com/og-kapama-fiyatlari",
    "https://gataelektrik.com/ketenci-fiyat-listesi",
    "https://gataelektrik.com/3m-og-ag-kablo-basliklari",
    "https://gataelektrik.com/woer-makaron-fiyat",
    "https://gataelektrik.com/safak-2022-fiyat-listesi",
    "https://gataelektrik.com/mutlusan-2021-kanal-fiyat",
    "https://gataelektrik.com/birtas-kablo-fiyat",
    "https://gataelektrik.com/herkules-kablo-fiyat",
    "https://gataelektrik.com/elektrik-panolari",
    "https://gataelektrik.com/yavuz-pano-fiyat-listesi",
    "https://gataelektrik.com/montajli-panolar",
    "https://gataelektrik.com/ensmet-fiyat-listesi",
    "https://gataelektrik.com/hensel-2021-fiyat-listesi",
    "https://gataelektrik.com/delta-inverter-fiyat",
    "https://gataelektrik.com/mervesan-fiyat-listesi",
    "https://gataelektrik.com/metop-fiyat-listesi-2022",
    "https://gataelektrik.com/abb-salt-2021-fiyat",
    "https://gataelektrik.com/siemens-otomasyon-2020",
    "https://gataelektrik.com/schneider-salt-fiyat",
    "https://gataelektrik.com/legrand-salt-fiyat",
    "https://gataelektrik.com/lg-salt-fiyat-listesi",
    "https://gataelektrik.com/hyundai-salt-fiyat-listesi",
    "https://gataelektrik.com/lovato-fiyat-listesi",
    "https://gataelektrik.com/viko-fiyat-listesi-2022",
    "https://gataelektrik.com/federal-salt-fiyat-listesi",
    "https://gataelektrik.com/tense-role-2022-fiyat-listesi",
    "https://gataelektrik.com/entes-fiyat-listesi-2021",
    "https://gataelektrik.com/emas-fiyat-listesi",
    "https://gataelektrik.com/ekon-kondansator-2021",
    "https://gataelektrik.com/finder-role-fiyat",
    "https://gataelektrik.com/tes-olcu-aletleri",
    "https://gataelektrik.com/burotik-priz-gruplari",
    "https://gataelektrik.com/ack-led-fiyat-2021",
    "https://gataelektrik.com/philips-aydinlatma",
    "https://gataelektrik.com/gecem-aydinlatma",
    "https://gataelektrik.com/telekom-fiyatlar-2021",
    "https://gataelektrik.com/osram-fiyat-listesi",
    "https://gataelektrik.com/vimar-fiyat-listesi-2021",
    "https://gataelektrik.com/vimar-idea",
    "https://gataelektrik.com/vimar-arke",
    "https://gataelektrik.com/thea-artline-fiyatlari"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Linklerden aranacak bilinen markaların listesi
bilinen_markalar = [
    "prysmian", "hes", "3m", "woer", "safak", "mutlusan", "birtas", "herkules", 
    "yavuz", "ensmet", "hensel", "delta", "mervesan", "metop", "abb", "siemens", 
    "schneider", "legrand", "lg", "hyundai", "lovato", "viko", "federal", "tense", 
    "entes", "emas", "ekon", "finder", "tes", "ack", "philips", "gecem", "osram", 
    "vimar", "thea", "ketenci"
]

tum_fiyatlar = []

print("Fiyat taraması başlıyor...")

for url in urls:
    print(f"Taranıyor: {url}")
    
    # URL içinden markayı tahmin etme mantığı
    url_parcasi = url.split("/")[-1].lower()
    marka = "Genel" # Eğer listede marka bulamazsa "Genel" yazacak
    
    for m in bilinen_markalar:
        if m in url_parcasi:
            # Marka isimlerinin baş harfini büyüt (Örn: schneider -> Schneider)
            # Eğer 3m, abb, lg gibi kısaltmaysa tamamını büyük harf yap
            if m in ["3m", "abb", "lg", "ack", "tes"]:
                marka = m.upper()
            else:
                marka = m.capitalize()
            break

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        satirlar = soup.find_all("tr")
        
        for satir in satirlar:
            sutunlar = satir.find_all("td")
            if len(sutunlar) >= 2:
                urun_adi = sutunlar[0].text.strip()
                fiyat = sutunlar[1].text.strip()
                
                if urun_adi and fiyat:
                    # Artık JSON listemize 'marka' sütununu da ekliyoruz
                    tum_fiyatlar.append({
                        "marka": marka,
                        "urun_adi": urun_adi,
                        "fiyat": fiyat
                    })
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")

with open("fiyatlar.json", "w", encoding="utf-8") as dosya:
    json.dump(tum_fiyatlar, dosya, ensure_ascii=False, indent=4)

print("İşlem tamamlandı! Veriler marka bilgisiyle fiyatlar.json dosyasına kaydedildi.")
