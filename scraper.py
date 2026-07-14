import requests
from bs4 import BeautifulSoup
import json
import time

# Senin verdiğin 50 sayfalık liste
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

# Bot olarak algılanmamak için tarayıcı taklidi yapıyoruz
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
        
        # NOT: Buradaki HTML etiketleri (td, div vb.) sitenin yapısına göre güncellenecektir.
        # Şimdilik örnek olarak tablolardaki satırları (tr) arıyoruz.
        satirlar = soup.find_all("tr")
        
        for satir in satirlar:
            sutunlar = satir.find_all("td")
            if len(sutunlar) >= 2:
                urun_adi = sutunlar[0].text.strip()
                fiyat = sutunlar[1].text.strip()
                
                # Eğer ürün adı veya fiyat boş değilse listeye ekle
                if urun_adi and fiyat:
                    tum_fiyatlar.append({
                        "kategori_linki": url,
                        "urun_adi": urun_adi,
                        "fiyat": fiyat
                    })
        
        # Sunucuyu yormamak ve engellenmemek için 3 saniye bekle
        time.sleep(3)
        
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")

# Verileri JSON dosyasına kaydet
with open("fiyatlar.json", "w", encoding="utf-8") as dosya:
    json.dump(tum_fiyatlar, dosya, ensure_ascii=False, indent=4)

print("İşlem tamamlandı! Veriler fiyatlar.json dosyasına kaydedildi.")
