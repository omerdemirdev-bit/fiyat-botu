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
        
        aktif_marka = "Genel"
        
        for eleman in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'strong', 'b', 'font', 'div', 'p', 'tr']):
            
            # 1. Eğer eleman bir tablo satırıysa
            if eleman.name == 'tr':
                sutunlar = eleman.find_all(["th", "td"])
                
                if len(sutunlar) == 1 and sutunlar[0].text.strip():
                    alt_baslik = sutunlar[0].text.strip()
                    if len(alt_baslik) < 80:
                        aktif_marka = alt_baslik.split()[0]
                
                elif len(sutunlar) >= 2:
                    urun_adi = sutunlar[0].text.strip()
                    fiyat = sutunlar[1].text.strip()
                    
                    gecersiz = ["ürün", "fiyat", "cinsi", "açıklama", "malzeme", "kodu"]
                    if urun_adi and fiyat:
                        if not any(k in urun_adi.lower() for k in gecersiz) and not any(k in fiyat.lower() for k in gecersiz):
                            tum_fiyatlar.append({
                                "marka": aktif_marka,
                                "urun_adi": urun_adi,
                                "fiyat": fiyat
                            })
                continue

            # 2. Tablo dışındaki metinlerde KESİN RENK KONTROLÜ
            if eleman.find_parent(['table', 'tr', 'td']):
                continue
                
            stil = eleman.get('style', '').lower()
            renk_attr = eleman.get('color', '').lower() if eleman.has_attr('color') else ''
            
            # Sadece Kırmızı ve Sarı renklerin kodları veya kelimeleri
            kirmizi_sari_kodlari = ['red', 'yellow', '#ff0000', '#ffff00', 'rgb(255, 0, 0)', 'rgb(255, 255, 0)', 'rgb(255,0,0)', 'rgb(255,255,0)']
            
            # Yazının stili içinde bu renklerden biri var mı?
            is_kirmizi_sari = any(renk in stil or renk in renk_attr for renk in kirmizi_sari_kodlari)
            
            # EĞER yazı kırmızı veya sarıysa (başlık falan olması umrumuzda değil)
            if is_kirmizi_sari:
                metin = eleman.text.strip()
                if metin and 2 < len(metin) < 80:
                    aktif_marka = metin.split()[0] # SADECE İLK KELİME
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")

with open("fiyatlar.json", "w", encoding="utf-8") as dosya:
    json.dump(tum_fiyatlar, dosya, ensure_ascii=False, indent=4)

print("İşlem tamamlandı! Yalnızca KIRMIZI ve SARI yazılar marka olarak kaydedildi.")
