# Web Scraping & Geocoding Platform

## Özellikler
- ScrapingBee API ile seyahat destinasyon verisi çekme
- Herhangi bir .json dosyasını seçip işleyebilme (output.json, changed.json, vb.)
- Gemini AI ile otomatik etiketleme (çıktı: labeled_output.json)
- Seçilen dosya için otomatik coğrafi kodlama (geocoding_cli.py arka planda çalışır)
- OpenStreetMap üzerinde tüm bulunan koordinatları pop-up ile gösterme
- Eksik kalan lokasyonları harita altında ayrı listede gösterme
- Şehir ve semt/ilçe bilgisi kullanıcıdan alınabilir (varsayılan: İstanbul/Türkiye)
- Modern, kullanıcı dostu ve gerçek zamanlı geri bildirimli Streamlit arayüzü
- API anahtarları .env dosyasında tutulur (gizli)
- Kapsamlı hata yönetimi ve veri doğrulama

## Kullanım
1. `requirements.txt` ile bağımlılıkları yükleyin.
2. `.env` dosyasına API anahtarınızı ekleyin.
3. `streamlit run sbee_streamlit.py` ile uygulamayı başlatın.
4. Arayüzden .json dosyası seçin, etiketleme ve/veya coğrafi kodlama işlemlerini başlatın.
5. Sonuçları harita ve listeler üzerinden inceleyin.

## Dosya Açıklamaları
- `sbee_streamlit.py`: Ana Streamlit uygulaması
- `geocoding_cli.py`: Komut satırı coğrafi kodlama aracı (Streamlit arayüzünden otomatik tetiklenir)
- `ScrapingBee/`: Scraping ve cache modülleri
- `output.json`, `changed.json`, `labeled_output.json`: Veri dosyaları
- `requirements.txt`: Gerekli Python paketleri

## Güvenlik ve Gizlilik
- API anahtarları kodda yer almaz, .env dosyasında tutulur.
- README ve kodda hassas bilgi bulunmaz.

## Sık Sorulanlar
- Herhangi bir .json dosyası ile çalışabilir miyim? **Evet.**
- Coğrafi kodlama için şehir/semt değiştirebilir miyim? **Evet, arayüzden girebilirsiniz.**
- Etiketleme çıktısı nereye kaydediliyor? **labeled_output.json**

```bash
# Clone the repository
git clone <repository-url>
cd web_scraping

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
# ScrapingBee API Configuration
SCRAPINGBEE_KEY=your_scrapingbee_api_key_here

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Geographic Coding APIs (Optional)
OPENCAGE_API_KEY=your_opencage_api_key_here
```

### 3. Run the Application

```bash
streamlit run sbee_streamlit.py
```

## 📋 Usage Guide

### Step 1: Web Scraping
1. Enter a website URL in the input field
2. Click "🚀 Fetch and Parse Data"
3. The system will extract travel destinations and save them to `output.json`

### Step 2: Destination Selection
1. Review the extracted destinations
2. Select destinations to remove (optional)
3. Click "💾 Save as changed.json" to save filtered data

### Step 3: AI Labeling
1. Click "🔍 Test Gemini API Connection" to verify API access
2. Click "🤖 Generate Labels with Gemini" to process destinations
3. View labeled results in the beautiful interface

### Step 4: Geographic Coding
1. Select any JSON file in the "Etiketlenmiş veriyle devam et" mode
2. Click "📍 Kordinatları bul, haritada göster" to run geocoding and display results
3. Found locations are shown on an interactive map with pop-ups (title, lat/lon)
4. Missing locations are listed below the map

## 📁 Project Structure

```
web_scraping/
├── sbee_streamlit.py          # Main Streamlit application
├── geocoding_system.py        # Geographic coding system
├── gemini_labeler.py          # Gemini AI labeling module
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── output.json                # Original scraped data
├── changed.json               # Filtered data for labeling
├── labeled_output.json        # Final labeled data (user-named .json files also possible)
├── ...                        # Other example or user-named labeled data
├── cache/                     # HTML cache directory
├── ScrapingBee/               # ScrapingBee package
└── ...
```

## 🔧 Configuration

### API Keys Required

1. **ScrapingBee API Key**: Get from [ScrapingBee](https://app.scrapingbee.com/)
2. **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/)
3. **OpenCage API Key** (Optional): Get from [OpenCage](https://opencagedata.com/) for enhanced geocoding
### Environment Variables

```env
SCRAPINGBEE_KEY=your_scrapingbee_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here
```

## 🎨 Features

### Modern UI Design
- Gradient backgrounds and animations
- Responsive card layouts
- Color-coded status indicators
- Interactive buttons with hover effects

### Smart Data Processing
- Automatic content extraction from HTML
- Intelligent text parsing and cleaning
- Efficient caching to reduce API calls
- Error handling and user feedback

### AI-Powered Labeling
- Context-aware label selection (up to 3 labels per destination)
- Fallback mechanisms for API errors

### Geographic Coding System
- 4-stage progressive geocoding approach
- OpenStreetMap integration via Nominatim
- Enhanced queries with fuzzy matching
- Optional API integrations (OpenCage, LocationIQ)
- Interactive map visualization with pop-ups
- Progress tracking and result management

## 📊 Output Format

### Input (`changed.json`)
```json
[
  {
    "title": "Destination Name",
    "content": "Description of the destination..."
  }
]
```

### Output (`labeled_output.json`)
```json
[
  {
    "title": "Destination Name",
    "content": "Description of the destination...",
    "labels": ["Plaj", "Aile Dostu", "Ekonomik"]
  }
]
```

## 🛠️ Development

### Adding New Labels

You can customize label logic in `gemini_labeler.py` if needed.

### Customizing the UI

Modify the CSS in `sbee_streamlit.py` to change colors, fonts, and layouts.

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check your API keys in `.env` file
   - Verify API quotas and billing
   - Test connection using the built-in test button

2. **No Data Extracted**
   - Check if the URL is accessible
   - Verify the website structure
   - Try different URLs

3. **Labels Not Generated**
   - Ensure Gemini API is working
   - Check API quotas
   - Verify the `changed.json` file exists

## 📈 Performance Tips

- Use caching to minimize API calls
- Process data in batches for large datasets
- Monitor API quotas to avoid rate limits
- Test with small datasets first

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [ScrapingBee](https://scrapingbee.com/) for web scraping API
- [Google Gemini](https://ai.google.dev/) for AI labeling
- [Streamlit](https://streamlit.io/) for the web interface
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing 

## 🆕 Version History

### [Yeni Sürüm] - Güncel Değişiklikler
- Herhangi bir .json dosyasından otomatik koordinat bulma ve haritada gösterme özelliği eklendi
- "Kordinatları bul, haritada göster" butonu ile seçilen dosya üzerinden geocoding_cli.py otomatik çalışır
- Bulunan lokasyonlar OpenStreetMap üzerinde pop-up'lı olarak gösterilir
- Bulunamayan lokasyonlar ayrı bir bilgi kutusunda listelenir
- Şehir ve ülke inputları kaldırıldı, otomatik olarak İstanbul/Türkiye kullanılır
- Modern hata yönetimi ve kullanıcıya anlık bilgilendirme eklendi
- Kullanıcı deneyimi ve arayüz akışı sadeleştirildi 
