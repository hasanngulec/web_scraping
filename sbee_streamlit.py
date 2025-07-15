import streamlit as st
from ScrapingBee.scrapingbee_cache import get_html
from bs4 import BeautifulSoup
import json
import os
from gemini_labeler import test_gemini_connection, process_changed_json
import time
import folium
from geopy.geocoders import Nominatim
from streamlit.components.v1 import html
from geocoding_system import GeocodingSystem
import subprocess

# --- Robust session state initialization (fixes KeyError) ---
if 'places' not in st.session_state:
    st.session_state['places'] = []
if 'remove_indices' not in st.session_state:
    st.session_state['remove_indices'] = []
if 'geocoding_system' not in st.session_state:
    st.session_state['geocoding_system'] = GeocodingSystem()
if 'selected_geocoding_file' not in st.session_state:
    st.session_state['selected_geocoding_file'] = None

# Page configuration
st.set_page_config(
    page_title="Web Scraper & Labeler",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .gemini-button > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .gemini-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .error-card {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .label-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .destination-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .title-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex: 1;
        margin: 0 0.5rem;
    }
    .stat-card h3, .stat-card h2 {
        color: #111 !important;
        text-shadow: none !important;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

def parse_destinations(html: str) -> list[dict]:
    """
    Extracts destination titles (h2 or h3) and their paragraph texts from HTML,
    returns as [{'title': ..., 'content': ...}, ...].
    """
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for header in soup.find_all(["h2", "h3"]):
        title = header.get_text(strip=True)
        paragraphs = []
        for sib in header.find_next_siblings():
            if sib.name in ["h2", "h3"]:
                break
            if sib.name == "p":
                text = sib.get_text(strip=True)
                if text:
                    paragraphs.append(text)
        if paragraphs:
            data.append({
                "title": title,
                "content": " ".join(paragraphs)
            })
    return data

def display_labeled_data(data):
    """Display labeled data in a beautiful format, with optional map/geocoding support"""
    if not data:
        st.warning("No labeled data to display")
        return

    # Statistics
    total_items = len(data)
    items_with_labels = sum(1 for item in data if item.get('labels'))
    total_labels = sum(len(item.get('labels', [])) for item in data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>📊 Total Items</h3>
            <h2>{total_items}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>🏷️ Items with Labels</h3>
            <h2>{items_with_labels}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>🎯 Total Labels</h3>
            <h2>{total_labels}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Her bir öğeyi göster
    for i, item in enumerate(data):
        with st.container():
            st.markdown(f"""
            <div class="destination-card">
                <h2 style='color:#222;font-size:2rem;font-weight:800;margin-bottom:0.5rem;'>📍 {item.get('title', 'Untitled')}</h2>
            """, unsafe_allow_html=True)
            st.write(item.get('content', 'No content'))
            labels = item.get('labels', [])
            if labels:
                st.markdown("<h4>🏷️ Labels:</h4>", unsafe_allow_html=True)
                label_html = ""
                for label in labels:
                    label_html += f'<span class="label-badge">{label}</span>'
                st.markdown(label_html, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #666; font-style: italic;'>No labels assigned</p>", unsafe_allow_html=True)
            # Debug: Gemini yanıtı ve fallback sonucu (varsa)
            if 'gemini_raw' in item:
                st.markdown(f"<div style='font-size:0.8em;color:#888;'>Gemini yanıtı: {item['gemini_raw']}</div>", unsafe_allow_html=True)
            if 'fallback_labels' in item:
                st.markdown(f"<div style='font-size:0.8em;color:#888;'>Fallback: {item['fallback_labels']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

def run_geocoding_cli(input_file: str, city: str = "İstanbul", country: str = "Türkiye", district: str = "") -> tuple[str, str]:
    """
    Seçili dosya ile geocoding_cli.py'yi çalıştırır. Çıktı dosyalarının adını döner.
    """
    resolved = "coor_resolved.json"
    remaining = "coor_remaining.json"
    cmd = [
        "python3", "geocoding_cli.py",
        "--in", input_file,
        "--city", city,
        "--country", country,
        "--out-resolved", resolved,
        "--out-remaining", remaining
    ]
    if district:
        cmd += ["--district", district]
    subprocess.run(cmd, check=True)
    return resolved, remaining

# --- Coğrafi Kodlama Butonu ve Arayüzü (EN ALTA) ---
    st.markdown("---")
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    show_geocoding = st.button("📍 Kordinatları belirle, haritada göster", key="geocoding_button")
    st.markdown("</div>", unsafe_allow_html=True)

    if show_geocoding:
        selected_file = st.session_state.get('selected_labeled_file', None)
        if not selected_file:
            st.warning("Önce etiketlenmiş veri dosyası seçmelisiniz.")
            return
        city = st.text_input("Şehir (isteğe bağlı, ör: İstanbul):", value=st.session_state.get('geocoding_city', ''))
        country = st.text_input("Ülke (isteğe bağlı, ör: Türkiye):", value=st.session_state.get('geocoding_country', 'Türkiye'))
        st.session_state['geocoding_city'] = city
        st.session_state['geocoding_country'] = country
        with st.spinner("Geocoding işlemi başlatılıyor ve koordinatlar bulunuyor..."):
            try:
                resolved_path, remaining_path = run_geocoding_cli(selected_file, city, country)
                st.success("Geocoding işlemi tamamlandı!")
                # coor_resolved.json'u oku ve haritada göster
                with open(resolved_path, "r", encoding="utf-8") as f:
                    resolved_data = json.load(f)
                locations = []
                for item in resolved_data:
                    coords = item.get("coordinates")
                    if coords and coords.get("latitude") is not None and coords.get("longitude") is not None:
                        locations.append({
                            "title": item.get("title", "(Başlıksız)"),
                            "lat": coords["latitude"],
                            "lon": coords["longitude"]
                        })
                if locations:
                    st.markdown("#### 🗺️ Bulunan Lokasyonlar Haritası")
                    m = folium.Map(location=[locations[0]["lat"], locations[0]["lon"]], zoom_start=13)
                    for loc in locations:
                        popup_text = f"<b>{loc['title']}</b><br>Lat: {loc['lat']:.6f}<br>Lon: {loc['lon']:.6f}"
                        folium.Marker([loc["lat"], loc["lon"]], popup=popup_text).add_to(m)
                    folium_html = m._repr_html_()
                    html(folium_html, height=600)
                else:
                    st.info("Hiçbir lokasyonun koordinatı bulunamadı.")
                # coor_remaining.json'u oku ve listele
                with open(remaining_path, "r", encoding="utf-8") as f:
                    remaining_data = json.load(f)
                if remaining_data:
                    st.markdown("#### ❌ Bulunamayan Lokasyonlar")
                    for item in remaining_data:
                        st.info(f"{item.get('title', '(Başlıksız)')}")
                else:
                    st.success("Tüm lokasyonlar başarıyla bulundu!")
            except Exception as e:
                st.error(f"Geocoding işlemi sırasında hata oluştu: {str(e)}")

# Main application
# --- Startup selection logic ---
if 'startup_mode' not in st.session_state:
    st.session_state['startup_mode'] = None

if st.session_state['startup_mode'] is None:
    st.markdown("""
    <div class="title-header">
        <h1>🌐 Web Scraper & AI Labeler</h1>
        <p>Lütfen bir seçenek seçin:</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Farklı bir link scrape etmek için tıklayınız", key="scrape_mode"):
            st.session_state['startup_mode'] = 'scrape'
            st.rerun()
    with col2:
        if st.button("📂 Etiketlenmiş veriyle devam et", key="labeled_mode"):
            st.session_state['startup_mode'] = 'labeled'
            st.rerun()
    st.stop()

# --- Labeled data mode: list and select among all labeled .json files ---
if st.session_state['startup_mode'] == 'labeled':
    import glob
    st.markdown("""
    <div class="title-header">
        <h1>📂 Etiketlenmiş Veriler</h1>
        <p>Mevcut etiketlenmiş veri dosyalarından birini seçebilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)
    exclude = {"output.json", "changed.json", "requirements.txt", "README.md", "README_rules.md", ".cursorrules"}
    json_files = [f for f in glob.glob("*.json") if os.path.basename(f) not in exclude]
    if not json_files:
        st.warning("Kök dizinde hiç etiketlenmiş veri dosyası bulunamadı.")
        st.stop()
    default_file = "labeled_output.json" if "labeled_output.json" in json_files else json_files[0]
    selected_file = st.selectbox("Bir etiketlenmiş veri dosyası seçin:", json_files, index=json_files.index(default_file) if default_file in json_files else 0, key="labeled_file_select")
    st.session_state['selected_labeled_file'] = selected_file
    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            labeled_data = json.load(f)
        display_labeled_data(labeled_data)
    except Exception as e:
        st.error(f"Seçilen dosya okunamadı: {str(e)}")
        st.stop()

    # --- Kordinatları bul, haritada göster butonu ve harita ---
    st.markdown("---")
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    city = st.text_input("Şehir (ör: İstanbul, İzmir, Ankara):", value=st.session_state.get("geocoding_city", "İstanbul"), key="city_input")
    district = st.text_input("Semt/İlçe/Mahalle (isteğe bağlı, ör: Balat, Alaçatı, Çeşme):", value=st.session_state.get("geocoding_district", ""), key="district_input")
    country = "Türkiye"
    # İşlem sırasında butonu devre dışı bırakmak için bir flag kullan
    if "geocoding_in_progress" not in st.session_state:
        st.session_state["geocoding_in_progress"] = False
    if "geocoding_result" not in st.session_state:
        st.session_state["geocoding_result"] = None
    start_geocoding = st.button("Geocoding işlemini başlat", key="start_geocoding_button", disabled=st.session_state["geocoding_in_progress"])
    st.markdown("</div>", unsafe_allow_html=True)

    if start_geocoding and not st.session_state["geocoding_in_progress"]:
        st.session_state["geocoding_in_progress"] = True
        st.session_state["geocoding_city"] = city
        st.session_state["geocoding_district"] = district
        with st.spinner("Geocoding işlemi başlatılıyor ve koordinatlar bulunuyor..."):
            try:
                resolved_path, remaining_path = run_geocoding_cli(selected_file, city, country, district)
                # coor_resolved.json'u oku ve harita/sonuçları session_state'e kaydet
                with open(resolved_path, "r", encoding="utf-8") as f:
                    resolved_data = json.load(f)
                with open(remaining_path, "r", encoding="utf-8") as f:
                    remaining_data = json.load(f)
                st.session_state["geocoding_result"] = {
                    "resolved": resolved_data,
                    "remaining": remaining_data
                }
                st.success("Geocoding işlemi tamamlandı!")
            except Exception as e:
                st.session_state["geocoding_result"] = {"error": str(e)}
                st.error(f"Geocoding işlemi sırasında hata oluştu: {str(e)}")
        st.session_state["geocoding_in_progress"] = False

    # Sonuçları göster
    result = st.session_state.get("geocoding_result", None)
    if result:
        if "error" in result:
            st.error(f"Geocoding işlemi sırasında hata oluştu: {result['error']}")
        else:
            resolved_data = result["resolved"]
            remaining_data = result["remaining"]
            locations = []
            for item in resolved_data:
                coords = item.get("coordinates")
                if coords and coords.get("latitude") is not None and coords.get("longitude") is not None:
                    locations.append({
                        "title": item.get("title", "(Başlıksız)"),
                        "lat": coords["latitude"],
                        "lon": coords["longitude"]
                    })
            if locations:
                st.markdown("#### 🗺️ Bulunan Lokasyonlar Haritası")
                m = folium.Map(location=[locations[0]["lat"], locations[0]["lon"]], zoom_start=13)
                for loc in locations:
                    popup_text = f"<b>{loc['title']}</b><br>Lat: {loc['lat']:.6f}<br>Lon: {loc['lon']:.6f}"
                    folium.Marker([loc["lat"], loc["lon"]], popup=popup_text).add_to(m)
                folium_html = m._repr_html_()
                html(folium_html, height=600)
            else:
                st.info("Hiçbir lokasyonun koordinatı bulunamadı.")
            if remaining_data:
                st.markdown("#### ❌ Bulunamayan Lokasyonlar")
                for item in remaining_data:
                    st.info(f"{item.get('title', '(Başlıksız)')}")
            else:
                st.success("Tüm lokasyonlar başarıyla bulundu!")
    st.stop()

# --- Scrape new link mode (classic flow) ---
st.markdown("### 🔗 Enter Website URL")
url = st.text_input("URL:", placeholder="https://example.com")

# Fetch and parse button
if st.button("🚀 Fetch and Parse Data", key="fetch_button"):
    if not url:
        st.error("Please enter a URL first!")
    else:
        with st.spinner("🔄 Fetching and processing data..."):
            try:
                html = get_html(url)
                st.session_state["places"] = parse_destinations(html)
                st.session_state["remove_indices"] = []  # Reset selections on each fetch
                
                # Save original data as output.json
                with open("output.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state["places"], f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ Successfully processed {len(st.session_state['places'])} destinations!")
                
            except Exception as e:
                st.error(f"❌ Error processing URL: {str(e)}")

places = st.session_state["places"]

if places:
    st.markdown("### 📋 Destination Selection")
    st.markdown(f"""
    <div class="info-card">
        <h4>📊 Found {len(places)} destinations!</h4>
        <p>Select the destinations you want to keep for labeling.</p>
    </div>
    """, unsafe_allow_html=True)
    
    titles = [f"{i+1}: {item['title']}" for i, item in enumerate(places)]
    remove_indices = st.multiselect(
        "❌ Select destinations to REMOVE:",
        options=list(range(len(places))),
        format_func=lambda i: titles[i],
        key="remove_indices"
    )
    
    filtered_places = [item for i, item in enumerate(places) if i not in remove_indices]
    
    st.markdown(f"""
    <div class="success-card">
        <h4>✅ {len(filtered_places)} destinations selected for processing</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Save as changed.json button
    if st.button("💾 Save as changed.json", key="save_button"):
        with open("changed.json", "w", encoding="utf-8") as f:
            json.dump(filtered_places, f, ensure_ascii=False, indent=2)
        
        st.markdown("""
        <div class="success-card">
            <h4>✅ changed.json file saved successfully!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if changed.json exists and show Gemini button
        if os.path.exists("changed.json"):
            st.session_state["changed_json_ready"] = True

# Gemini labeling section
if os.path.exists("changed.json") or st.session_state.get("changed_json_ready", False):
    st.markdown("### 🤖 AI Labeling with Gemini")
    
    # Test Gemini API connection
    if st.button("🔍 Test Gemini API Connection", key="test_api"):
        with st.spinner("Testing API connection..."):
            if test_gemini_connection():
                st.markdown("""
                <div class="success-card">
                    <h4>✅ Gemini API connection successful!</h4>
                </div>
                """, unsafe_allow_html=True)
                st.session_state["api_working"] = True
            else:
                st.markdown("""
                <div class="error-card">
                    <h4>❌ Gemini API connection failed!</h4>
                    <p>Please check your GEMINI_API_KEY in the .env file.</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state["api_working"] = False
    
    # Gemini labeling button
    if st.session_state.get("api_working", False):
        if st.button("🤖 Generate Labels with Gemini", key="gemini_button", help="Click to process changed.json and generate labels"):
            with st.spinner("🔄 Processing destinations with Gemini AI..."):
                try:
                    labeled_data = process_changed_json()
                    # Dosya adı sorma kısmını kaldır, otomatik kaydet
                    with open("labeled_output.json", "w", encoding="utf-8") as f:
                        json.dump(labeled_data, f, ensure_ascii=False, indent=2)
                    st.success("Etiketlenmiş veri labeled_output.json olarak kaydedildi!")
                    st.session_state["last_labeled_file"] = "labeled_output.json"
                    # Display the labeled data preview
                    st.markdown("### 📊 Labeled Results (Önizleme)")
                    display_labeled_data(labeled_data)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-card">
                        <h4>❌ Error generating labels</h4>
                        <p>{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-card">
            <h4>⚠️ API Connection Required</h4>
            <p>Please test the Gemini API connection first before generating labels.</p>
        </div>
        """, unsafe_allow_html=True)

# Display labeled data if it exists

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🌐 Web Scraper & AI Labeler | Powered by ScrapingBee & Gemini AI</p>
</div>
""", unsafe_allow_html=True)
