# 🆕 Sürüm Notları (Son Değişiklikler)
- Tüm .json dosyaları .gitignore ile versiyon kontrolünden hariç tutuldu
- coor_resolved.json ve coor_remaining.json dosyaları otomatik olarak yönetiliyor, repoda tutulmuyor
- LocationIQ API anahtarı desteği ve dokümantasyonu eklendi
- Arayüzde şehir/semt girişleri sadeleştirildi, varsayılan olarak İstanbul/Türkiye kullanılıyor
- Geocoding ve harita gösterimi tüm .json dosyaları için otomatikleştirildi
- Modern hata yönetimi ve kullanıcıya anlık bilgilendirme eklendi
- Kullanıcı deneyimi ve arayüz akışı sadeleştirildi

# Web Scraping Projesi CursorRules
# Cursor AI deneyimini geliştirmek için web scraping projelerinde kullanılan kural seti

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Cursor AI](https://img.shields.io/badge/Cursor-AI-blue)](https://cursor.sh)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/ScrapingBee-API-orange.svg" alt="ScrapingBee">
</div>

## 📋 Proje Açıklaması

Bu proje, ScrapingBee API kullanarak web scraping işlemleri yapan ve Streamlit arayüzü ile veri çıkarma ve analiz sağlayan bir web scraping projesidir. Proje, web sitelerinden destinasyon bilgilerini çıkarmaya ve kullanıcı dostu bir veri yönetimi arayüzü sağlamaya odaklanmıştır.

## 🤔 Neden .cursorrules?

`.cursorrules` dosyaları, Cursor AI'ın projenizle çalışırken takip etmesi gereken kuralları ve yönergeleri tanımlar. Bu dosya sayesinde:

- **Tutarlı kod stili** sağlanır
- **Proje-spesifik best practices** uygulanır
- **AI asistanı** projenizin yapısını anlar
- **Kod üretimi** projenizin ihtiyaçlarına uygun olur
- **Hata yönetimi** standartlaştırılır

## 📚 İçindekiler

- [Proje Yapısı Kuralları](#proje-yapısı-kuralları)
- [Kod Stili ve Konvansiyonlar](#kod-stili-ve-konvansiyonlar)
- [API ve Ortam Yönetimi](#api-ve-ortam-yönetimi)
- [Veri İşleme Rehberi](#veri-işleme-rehberi)
- [Test ve Kalite Güvencesi](#test-ve-kalite-güvencesi)
- [Dokümantasyon Standartları](#dokümantasyon-standartları)
- [Yaygın Pattern'ler ve Metodlar](#yaygın-patternler-ve-metodlar)
- [Hata Yönetimi Rehberi](#hata-yönetimi-rehberi)
- [Performans Değerlendirmeleri](#performans-değerlendirmeleri)
- [Güvenlik Best Practices](#güvenlik-best-practices)
- [Geliştirme İş Akışı](#geliştirme-iş-akışı)
- [Yaygın Kütüphaneler ve Bağımlılıklar](#yaygın-kütüphaneler-ve-bağımlılıklar)
- [Dosya İsimlendirme Konvansiyonları](#dosya-isimlendirme-konvansiyonları)
- [Kod Üretimi Tercihleri](#kod-üretimi-tercihleri)
- [Proje-Spesifik Bağlam](#proje-spesifik-bağlam)
- [AI Asistan Rehberi](#ai-asistan-rehberi)
- [Versiyonlama Protokolü](#versiyonlama-protokolü)

## 🏗️ Proje Yapısı Kuralları

Aşağıdaki proje yapısını her zaman koruyun:

```
web_scraping/
├── requirements.txt          # Ana proje dosyaları
├── README.md
├── README_rules.md          # Türkçe kurallar dokümantasyonu
├── .cursorrules             # Cursor AI kuralları (İngilizce)
├── .env.example
├── ScrapingBee/            # ScrapingBee paket dizini
│   └── scrapingbee_cache/  # scrapingbee_cache modülü
├── cache/                  # Önbelleklenmiş HTML dosyaları (otomatik oluşturulur)
├── sbee_streamlit.py       # Ana Streamlit uygulaması
├── output.json             # Orijinal çıkarılan veri
└── changed.json            # Filtrelenmiş/işlenmiş veri
```

### Dosya Organizasyon Kuralları

- Tüm ScrapingBee ile ilgili kodu `ScrapingBee/` dizininde tutun
- HTML dosyaları için ayrı cache dizini koruyun
- API anahtarları için `.env` dosyası kullanın (asla versiyon kontrolüne commit etmeyin)
- JSON çıktı dosyalarını kolay erişim için kök dizinde saklayın
- `README_rules.md` dosyasını Türkçe dokümantasyon için kullanın
- `.cursorrules` dosyasını İngilizce Cursor AI kuralları için kullanın

## 💻 Kod Stili ve Konvansiyonlar

### Python Kod Rehberi

- Tüm fonksiyon parametreleri ve dönüş değerleri için type hints kullanın
- PEP 8 stil rehberini takip edin
- Açıklayıcı değişken isimleri kullanın (örn. `html_content`, `parsed_data`)
- Tüm fonksiyonlara amaç ve parametreleri açıklayan docstring'ler ekleyin
- String formatlama için f-string'ler kullanın
- İstisnaları özel hata mesajlarıyla zarifçe yönetin

### Streamlit Uygulama Kuralları

- Etkileşimler arasında veri kalıcılığı için `session_state` kullanın
- `st.spinner()` ile uygun yükleme durumları uygulayın
- Kullanıcı geri bildirimi için `st.success()`, `st.error()`, `st.warning()` kullanın
- UI elementlerini mantıklı olarak organize edin (giriş → işleme → çıktı)
- Her zaman net kullanıcı talimatları ve geri bildirim sağlayın

### Web Scraping Best Practices

- Gereksiz API çağrılarını önlemek için her zaman önbellekleme uygulayın
- Uygun hata yönetimi ile BeautifulSoup kullanın
- Veriyi sistematik olarak çıkarın (başlık → içerik → metadata)
- İşlemeden önce çıkarılan veriyi doğrulayın
- Farklı HTML yapılarını zarifçe yönetin

## 🔧 API ve Ortam Yönetimi

- API anahtarlarını asla kaynak kodda hardcode etmeyin
- Ortam değişkeni yönetimi için `python-dotenv` kullanın
- API hataları için uygun hata yönetimi uygulayın
- Web istekleri için makul timeout'lar ayarlayın
- Kota kullanımını minimize etmek için API yanıtlarını önbellekleme yapın

## 📊 Veri İşleme Rehberi

- BeautifulSoup kullanarak HTML içeriğini sistematik olarak parse edin
- Yapılandırılmış veri çıkarın (başlık, içerik, metadata)
- Kaydetmeden önce veri doğrulaması uygulayın
- Uygun encoding ile JSON formatında veri saklama kullanın
- Veri filtreleme ve seçim yetenekleri sağlayın

## 🧪 Test ve Kalite Güvencesi

- Temel fonksiyonlar için unit testler yazın (parsing, caching)
- Çeşitli HTML yapılarıyla test edin
- API yanıtlarını ve hata yönetimini doğrulayın
- Streamlit arayüz etkileşimlerini test edin
- Kullanıcılar için uygun hata mesajları sağlayın

## 📖 Dokümantasyon Standartları

- Kurulum talimatları ile kapsamlı README.md koruyun
- API gereksinimlerini ve ortam kurulumunu dokümante edin
- Kullanım örnekleri ve ekran görüntüleri dahil edin
- Tüm bağımlılıklarla requirements.txt'yi güncel tutun
- Proje-spesifik konvansiyonları dokümante edin
- README_rules.md dosyasını Türkçe dokümantasyon için kullanın

## 🔄 Yaygın Pattern'ler ve Metodlar

### HTML Parsing Pattern

```python
def parse_destinations(html: str) -> list[dict]:
    """
    HTML'den destinasyon başlıklarını ve içeriğini çıkarır.
    Başlık ve içerik alanları ile yapılandırılmış veri döndürür.
    """
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for header in soup.find_all(["h2", "h3"]):
        # Başlık ve ilişkili içeriği çıkar
        # Yapılandırılmış veri döndür
    return data
```

### Caching Pattern

```python
def get_html(url: str) -> str:
    """
    Önbellekleme desteği ile HTML getirir.
    Önce cache'i kontrol eder, sonra gerekirse API'den çeker.
    """
    # Cache'i kontrol et
    # Cache'de yoksa API'den çek
    # Cache'e kaydet
    # İçeriği döndür
```

### Streamlit Session State Pattern

```python
# Session state'i başlat
if "data" not in st.session_state:
    st.session_state["data"] = []

# Session state'i güncelle
st.session_state["data"] = new_data

# Session state'i kullan
data = st.session_state["data"]
```

## ⚠️ Hata Yönetimi Rehberi

- API anahtarı mevcudiyetini her zaman kontrol edin
- Ağ timeout'larını zarifçe yönetin
- Parse etmeden önce HTML içeriğini doğrulayın
- Kullanıcı dostu hata mesajları sağlayın
- Hata ayıklama için hataları loglayın

## ⚡ Performans Değerlendirmeleri

- Pahalı işlemler için önbellekleme uygulayın
- Verimli HTML parsing metodları kullanın
- Önbellekleme ile API çağrılarını minimize edin
- Streamlit yeniden render'larını optimize edin
- Büyük veri setlerini verimli şekilde yönetin

## 🔒 Güvenlik Best Practices

- API anahtarlarını kod veya log'larda asla açığa çıkarmayın
- İşlemeden önce kullanıcı girdilerini doğrulayın
- Gerektiğinde HTML içeriğini sanitize edin
- Güvenli dosya işleme uygulamaları kullanın
- Uygun erişim kontrolleri uygulayın

## 🔄 Geliştirme İş Akışı

- Değişiklikleri geliştirme ortamında test edin
- Dağıtımdan önce API yanıtlarını doğrulayın
- Yeni özelliklerle dokümantasyonu güncelleyin
- Tutarlı kod formatlaması koruyun
- UI etkileşimlerini gözden geçirin ve test edin

## 📚 Yaygın Kütüphaneler ve Bağımlılıklar

- `streamlit`: Web uygulama framework'ü
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP client
- `python-dotenv`: Ortam yönetimi
- `replicate`: AI/ML entegrasyonu (gerekirse)

## 📝 Dosya İsimlendirme Konvansiyonları

- Fonksiyonlar ve değişkenler için açıklayıcı isimler kullanın
- Python dosyaları ve fonksiyonları için `snake_case` takip edin
- Uygun olduğunda JSON anahtarları için `camelCase` kullanın
- Proje genelinde tutarlı isimlendirme koruyun

## 🤖 Kod Üretimi Tercihleri

- Kapsamlı hata yönetimi üretin
- Tüm fonksiyonlar için type hints dahil edin
- Amaç ve kullanımı açıklayan docstring'ler ekleyin
- Anlamlı değişken isimleri kullanın
- Hata ayıklama için uygun logging uygulayın

## 🎯 Proje-Spesifik Bağlam

Bu proje şunlar için tasarlanmıştır:

- ScrapingBee API ile web scraping
- Seyahat/destinasyon web sitelerinden veri çıkarma
- Kullanıcı dostu veri filtreleme ve yönetimi
- API kullanımını optimize etmek için önbellekleme
- Streamlit tabanlı web arayüzü

## 🤖 AI Asistan Rehberi

Bu projeye yardım ederken:

- Web scraping ve veri işleme pattern'lerine odaklanın
- API kota sınırlamalarını ve önbellekleme stratejilerini göz önünde bulundurun
- Streamlit arayüzünde kullanıcı deneyimini önceliklendirin
- Veri bütünlüğü ve doğrulamasını koruyun
- Kurulmuş proje yapısını takip edin
- Değişikliklerin performans etkilerini göz önünde bulundurun
- Uygun hata yönetimi ve kullanıcı geri bildirimi sağlayın

## 🔄 Versiyonlama Protokolü

### Otomatik Versiyonlama Sistemi

Kullanıcı "Projenin bu halini versiyonla" dediğinde:

1. **Değişiklik Analizi**: Mevcut proje durumunu analiz et ve değişiklikleri tespit et
2. **Dosya Güncellemeleri**:
   - `README_rules.md`: Türkçe olarak güncelle
   - `.cursorrules`: İngilizce olarak güncelle
   - `README.md`: Versiyon değişikliklerini belgele
3. **Git İşlemleri**: Değişiklikleri commit et ve GitHub'a push et

### Versiyonlama Kuralları

- Her versiyonlama işleminde değişiklikleri detaylı olarak belgele
- Türkçe ve İngilizce dokümantasyonu senkronize tut
- Git commit mesajlarında açıklayıcı bilgiler kullan
- Versiyon numaralarını tutarlı şekilde artır

### Dosya Dilleri

- `README_rules.md`: 🇹🇷 Türkçe dokümantasyon
- `.cursorrules`: 🇺🇸 İngilizce Cursor AI kuralları
- `README.md`: Versiyon değişiklikleri ve genel bilgiler

## 🚀 Kullanım

Bu `.cursorrules` dosyasını projenizin kök dizinine yerleştirin. Cursor AI artık projenizle çalışırken bu kuralları takip edecektir.

## 📝 Katkıda Bulunma

Bu projeye katkıda bulunmak için:

1. Repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

**Not:** Bu `.cursorrules` dosyası, Cursor AI'ın projenizle çalışırken takip etmesi gereken kuralları tanımlar ve kod üretimini projenizin ihtiyaçlarına uygun hale getirir. 