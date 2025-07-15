# 🌐 Web Scraper & AI Labeler

A modern web scraping application with AI-powered labeling capabilities using ScrapingBee API and Google Gemini AI.

## ✨ Features

- **Web Scraping**: Extract travel destinations from any website using ScrapingBee API
- **AI Labeling**: Automatically label destinations using Google Gemini 1.5 Pro
- **Geographic Coding**: 4-stage geocoding system using OpenStreetMap and APIs
- **Modern UI**: Beautiful Streamlit interface with gradient designs and animations
- **Smart Caching**: Efficient caching system to minimize API calls
- **Comprehensive Labels**: 100+ predefined travel-related labels across 10 categories
- **Real-time Processing**: Live feedback and progress indicators
- **Interactive Maps**: Visualize locations with Folium maps

## 🚀 Quick Start

### 1. Installation

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
LOCATIONIQ_API_KEY=your_locationiq_api_key_here
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

### Step 4: Geographic Coding (Optional)
1. Select a labeled JSON file in the "Etiketlenmiş veriyle devam et" mode
2. Click "📍 Coğrafi Kodlama" to access the geocoding system
3. Choose from 4 different geocoding stages:
   - **Stage 1**: Basic Nominatim queries
   - **Stage 2**: Enhanced location queries with fuzzy matching
   - **Stage 3**: OpenCage API (requires API key)
   - **Stage 4**: Manual input preparation
4. View results on interactive maps

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
├── balat.json                 # Example user-named labeled data
├── labeled_output copy.json   # Example labeled data
├── cache/                     # HTML cache directory
│   └── https_www.bizevdeyokuz.com_balat-gezilecek-yerler_.html
├── ScrapingBee/               # ScrapingBee package
│   ├── scrapingbee_cache/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   └── utils.py
│   ├── setup.py
│   ├── README.md
│   └── tests/
│       └── test_cache.py
├── test_gemini.py             # Gemini test script
├── LICENSE
└── ...
```

## 🔧 Configuration

### API Keys Required

1. **ScrapingBee API Key**: Get from [ScrapingBee](https://app.scrapingbee.com/)
2. **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/)
3. **OpenCage API Key** (Optional): Get from [OpenCage](https://opencagedata.com/) for enhanced geocoding
4. **LocationIQ API Key** (Optional): Get from [LocationIQ](https://locationiq.com/) for alternative geocoding

### Environment Variables

```env
SCRAPINGBEE_KEY=your_scrapingbee_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here
LOCATIONIQ_API_KEY=your_locationiq_api_key_here
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
- Few-shot learning with examples
- Context-aware label selection
- Maximum 3 labels per destination
- Fallback mechanisms for API errors

### Geographic Coding System
- 4-stage progressive geocoding approach
- OpenStreetMap integration via Nominatim
- Enhanced queries with fuzzy matching
- Optional API integrations (OpenCage, LocationIQ)
- Interactive map visualization
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

Edit `gemini_labeler.py` and add new labels to the `LABEL_CATEGORIES` dictionary:

```python
LABEL_CATEGORIES = {
    "New Category": [
        "New Label 1",
        "New Label 2",
        "New Label 3"
    ]
}
```

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
- Birden fazla etiketlenmiş veri dosyası desteği eklendi
- Etiketleme sonrası kullanıcıdan dosya ismi alınarak .json olarak kaydedilebiliyor
- "Etiketlenmiş veriyle devam et" seçeneğinde, kök dizindeki tüm etiketli .json dosyaları listelenip seçilebiliyor
- Başlangıçta iki seçenekli (yeni scraping veya etiketli veriyle devam) kullanıcı akışı eklendi
- labeled_output.json varsayılan olarak seçili geliyor (varsa)
- Modern ve görünür özet kartları, hata yönetimi ve kullanıcı deneyimi iyileştirildi 