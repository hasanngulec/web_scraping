# Web Scraping Projesi - Kural ve Sürüm Notları

## Son Sürümdeki Temel Değişiklikler
- Herhangi bir .json dosyası (output.json, changed.json, vb.) ile çalışabilme
- Seçilen dosya için coğrafi kodlama (geocoding_cli.py otomatik çalışır)
- Bulunan koordinatların OpenStreetMap üzerinde pop-up ile gösterimi
- Eksik kalan lokasyonların harita altında ayrı listelenmesi
- Şehir ve semt/ilçe bilgisi arayüzden kullanıcı tarafından girilebilir (varsayılan: İstanbul/Türkiye)
- Gemini etiketleme çıktısı otomatik olarak labeled_output.json'a kaydedilir
- Modern ve kullanıcı dostu Streamlit arayüzü, gerçek zamanlı geri bildirim
- README ve kodda hassas/silinmiş dosya veya bilgi bulunmaz

## Proje Kuralları
- API anahtarları .env dosyasında tutulur, kodda yer almaz
- Her .json dosyası ile çalışılabilir
- Coğrafi kodlama ve harita gösterimi entegre edilmiştir
- Etiketleme işlemi sonrası çıktı dosyası otomatik kaydedilir
- Kullanıcıdan şehir/semt bilgisi alınabilir, kodda sabit değildir
- Arayüzde tüm işlemler için net geri bildirim ve hata yönetimi sağlanır

## Sürüm Geçmişi
- [Güncel] Coğrafi kodlama ve harita entegrasyonu, dosya seçme esnekliği, genel arayüz iyileştirmeleri

## Lisans
MIT 