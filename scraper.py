import requests
from bs4 import BeautifulSoup
import json
import time
import re

# Sitedeki geçerli markaların tam listesi
resmi_markalar = [
    "Hitachi", "Tedaş", "Astor", "Eaton", "Best/Eltaş", "Schneider", "Legrand",
    "Gata", "Sarkuysan Bakır", "Pyrsmian", "Hes", "Öznur", "Hasçelik", "Kauçuk",
    "Ketenci", "3M", "Woer", "Tügen", "Birtaş", "Herkül", "tongün", "Yavuz Pano",
    "Ensmet", "Güçtay", "Hensel", "Delta", "Mervesan", "Metop", "ABB", "Siemens",
    "LS", "Hyundai", "Lovato", "Viko", "Federal", "Tense", "Entes", "Emas", "Ekon",
    "Finder", "Nexans", "Fluke", "ACK", "Yavuz", "Gecem", "Hikvision", "İlker", "Vimar"
]

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

# Metin içinde marka arayan özel fonksiyon
def marka_tespit_et(metin, markalar):
    metin_kucuk = metin.lower()
    for marka in markalar:
        # Kelime bazlı arama yap (örneğin 'Hes' ararken 'Hesap' kelimesine takılmaması için)
        if re.search(r'\b' + re.escape(marka.lower()) + r'\b', metin_kucuk):
            return marka
    return None

print("Dinamik marka taraması başlıyor...")

for url in urls:
    print(f"Taranıyor: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        aktif_marka = "Genel" # Sayfaya girerken sıfırla
        
        # Sayfadaki her şeyi belge sırasına göre yukarıdan aşağıya tarıyoruz
        for eleman in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'span', 'strong', 'b', 'tr']):
            
            # Eğer eleman bir tablo satırıysa
            if eleman.name == 'tr':
                sutunlar = eleman.find_all(['th', 'td'])
                
                # Tek hücreli satırsa (tablo içindeki alt başlık veya marka adı olabilir)
                if len(sutunlar) == 1:
                    metin = sutunlar[0].get_text(" ", strip=True)
                    bulunan_marka = marka_tespit_et(metin, resmi_markalar)
                    if bulunan_marka:
                        aktif_marka = bulunan_marka # Yeni markayı hafızaya al
                
                # 2 veya daha fazla hücreliyse (ürün listesi)
                elif len(sutunlar) >= 2:
                    urun_adi = sutunlar[0].get_text(" ", strip=True)
                    fiyat = sutunlar[1].get_text(" ", strip=True)
                    
                    gecersiz_kelimeler = ["ürün", "fiyat", "cinsi", "açıklama", "malzeme", "kodu", "no"]
                    
                    if urun_adi and fiyat:
                        # Ürün adının veya fiyatın tablo başlığı ("Ürün Adı", "Liste Fiyatı" vb.) olmadığını doğrula
                        if not any(k in urun_adi.lower() for k in gecersiz_kelimeler) and not any(k in fiyat.lower() for k in gecersiz_kelimeler):
                            tum_fiyatlar.append({
                                "marka": aktif_marka, # Hafızadaki güncel markayı bas
                                "urun_adi": urun_adi,
                                "fiyat": fiyat
                            })
            
            # Eğer eleman tablo dışındaki bir başlıksa veya metinse
            else:
                # Tablonun içindeki yazıları 'tr' döngüsünde hallettiğimiz için burada atlıyoruz
                if eleman.find_parent('table'):
                    continue
                
                metin = eleman.get_text(" ", strip=True)
                # Sadece başlık olabilecek kısalıktaki metinleri tara (100 karakterden kısaysa)
                if metin and len(metin) < 100:
                    bulunan_marka = marka_tespit_et(metin, resmi_markalar)
                    if bulunan_marka:
                        aktif_marka = bulunan_marka # Yeni markayı hafızaya al
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")

with open("fiyatlar.json", "w", encoding="utf-8") as dosya:
    json.dump(tum_fiyatlar, dosya, ensure_ascii=False, indent=4)

print("İşlem tamamlandı! Sayfa içi listeler taranarak markalar dinamik olarak eşleştirildi.")
