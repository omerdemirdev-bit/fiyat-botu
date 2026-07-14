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

tum_fiyatlar = []

print("Fiyat taraması başlıyor...")

for url in urls:
    print(f"Taranıyor: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Varsayılan başlangıç markası olarak ana sayfa başlığını (h1) alalım
        aktif_marka = "Genel"
        h1 = soup.find("h1")
        if h1 and h1.text.strip():
            aktif_marka = h1.text.strip()
            
        # Sayfadaki tüm başlıkları (h2, h3, h4, h5) ve tablo satırlarını (tr) sayfadaki sırasına göre bul
        for eleman in soup.find_all(['h2', 'h3', 'h4', 'h5', 'tr']):
            
            # Eğer eleman bir başlıksa, yeni markamız bu başlık olsun
            if eleman.name in ['h2', 'h3', 'h4', 'h5']:
                baslik_metni = eleman.text.strip()
                if baslik_metni and len(baslik_metni) < 80: # Saçma sapan uzun metinleri elemek için
                    aktif_marka = baslik_metni
                    
            # Eğer eleman bir tablo satırıysa, hafızadaki son aktif markayı kullanarak ürünleri çek
            elif eleman.name == 'tr':
                sutunlar = eleman.find_all(["th", "td"])
                
                # Tablo içinde yine de tek satırlık alt başlıklar varsa onları da yakalayalım
                if len(sutunlar) == 1 and sutunlar[0].text.strip():
                    alt_baslik = sutunlar[0].text.strip()
                    if len(alt_baslik) < 80:
                        aktif_marka = alt_baslik
                    continue 

                # En az 2 sütun varsa fiyat verisidir
                if len(sutunlar) >= 2:
                    urun_adi = sutunlar[0].text.strip()
                    fiyat = sutunlar[1].text.strip()
                    
                    gecersiz_kelimeler = ["ürün", "fiyat", "cinsi", "açıklama", "malzeme"]
                    if urun_adi and fiyat:
                        # Tablo başlıkları "Ürün Adı", "Fiyatı" satırlarını JSON'a eklememek için filtreliyoruz
                        if not any(k in urun_adi.lower() for k in gecersiz_kelimeler) and not any(k in fiyat.lower() for k in gecersiz_kelimeler):
                            tum_fiyatlar.append({
                                "marka": aktif_marka,
                                "urun_adi": urun_adi,
                                "fiyat": fiyat
                            })
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")

with open("fiyatlar.json", "w", encoding="utf-8") as dosya:
    json.dump(tum_fiyatlar, dosya, ensure_ascii=False, indent=4)

print("İşlem tamamlandı! Veriler headline'lardan okunan marka bilgisiyle fiyatlar.json dosyasına kaydedildi.")
