# Hak Ticaret - Çil Teknik Ürün Arama Sistemi

Bu proje, Çil Teknik web sitesinden ürün verilerini çekip kullanıcı dostu bir arama arayüzü sunan web uygulamasıdır.

## 🚀 Özellikler

- **Otomatik Veri Çekme**: Çil Teknik web sitesinden ürün verilerini otomatik olarak çeker
- **Akıllı Arama**: Ürün adı ve koduna göre kelime bazlı arama
- **Detaylı Ürün Bilgileri**: 
  - Ürün kodu ve adı
  - USD ve TL fiyatları
  - Stok durumu (renkli gösterim)
  - Ürün resimleri
- **Akıllı Sıralama**: Stokta olan ürünler üstte gösterilir
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Son Güncelleme Bilgisi**: Verilerin ne zaman güncellendiğini gösterir

## 📁 Dosya Yapısı

```
cilteknik/
├── run.py          # Veri çekme scripti
├── index.html      # Web arayüzü
├── urunler.json    # Ürün verileri (otomatik oluşur)
└── README.md       # Bu dosya
```

## 🛠️ Kurulum

### Gereksinimler

```bash
pip install requests beautifulsoup4 flask
```

### Environment Değişkenleri

Çil Teknik giriş bilgilerinizi environment değişkenleri olarak tanımlayın:

```bash
export CILT_KULLANICI="kullanici_adiniz"
export CILT_SIFRE="sifreniz"
```

Windows için:
```cmd
set CILT_KULLANICI=kullanici_adiniz
set CILT_SIFRE=sifreniz
```

## 🚀 Kullanım

### 1. Veri Çekme

```bash
python run.py
```

Bu komut:
- Çil Teknik sitesine giriş yapar
- Tüm ürün verilerini çeker
- `urunler.json` dosyasına kaydeder
- UTC timezone ile timestamp ekler

### 2. Web Arayüzünü Başlatma

```bash
python -m http.server 8000
```

veya Flask ile:

```bash
python -c "from flask import Flask, send_from_directory; app = Flask(__name__); app.route('/')(lambda: send_from_directory('.', 'index.html')); app.route('/<path:filename>')(lambda filename: send_from_directory('.', filename)); app.run(host='0.0.0.0', port=8000, debug=True)"
```

Tarayıcınızda `http://localhost:8000` adresine gidin.

## 📊 Veri Yapısı

`urunler.json` dosyası şu yapıda veri içerir:

```json
{
    "last_updated": "2025-01-10 15:30:25",
    "data": [
        {
            "urun_kodu": "E0000512",
            "urun_adi": "FAN MOTORU PERVANE 200mm",
            "urun_id": "1",
            "resim": "/images/Urun/example.jpg",
            "fiyat": "1,30",
            "fiyat_birimi": "USD",
            "tl_liste_fiyati": "52,86",
            "stok_durumu": "1"
        }
    ]
}
```

## 🎨 Arayüz Özellikleri

### Arama
- En az 2 karakter ile arama başlar
- Kelime bazlı arama (tüm kelimeler ürün adında/kodunda olmalı)
- Gerçek zamanlı arama sonuçları

### Ürün Kartları
- **Sol taraf**: USD ve TL fiyatları
- **Sağ taraf**: Stok durumu (renkli badge)
- **Üstte**: Stokta olan ürünler
- **Altta**: Stokta olmayan ürünler

### Stok Durumu Renkleri
- 🟢 **Yeşil**: Stokta var
- 🔴 **Kırmızı**: Stokta yok

## 🔄 Otomatik Güncelleme

Web arayüzü her saat başı otomatik olarak JSON dosyasını yeniden yükler.

## ⚙️ Teknik Detaylar

- **Backend**: Python (requests, BeautifulSoup)
- **Frontend**: Vanilla JavaScript, CSS Grid, Flexbox
- **Data Format**: JSON
- **Timezone**: UTC (server) → TR (frontend)
- **Responsive**: Mobile-first design

## 📝 Notlar

- Environment değişkenlerini tanımlamadan script çalışmaz
- Çil Teknik sitesinin yapısı değişirse parser güncellenmesi gerekebilir
- JSON dosyası her çalıştırmada tamamen yenilenir
- Web arayüzü için internet bağlantısı gerekli (resimler için)

## 🐛 Sorun Giderme

### "Environment değişkenleri tanımlı değil" hatası
Environment değişkenlerini doğru tanımladığınızdan emin olun.

### "Login failed" hatası
Kullanıcı adı ve şifrenizi kontrol edin.

### Resimler görünmüyor
İnternet bağlantınızı kontrol edin ve Çil Teknik sitesinin erişilebilir olduğundan emin olun.

## 📄 Lisans

Bu proje kişisel kullanım içindir. Ticari kullanım için Çil Teknik'den izin alınmalıdır. 