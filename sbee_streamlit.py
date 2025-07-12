import streamlit as st
from ScrapingBee.scrapingbee_cache import get_html
from bs4 import BeautifulSoup
import json
import os
from gemini_labeler import test_gemini_connection, process_changed_json
import time

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
    """Display labeled data in a beautiful format"""
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
    
    # Display each item
    for i, item in enumerate(data):
        with st.container():
            st.markdown(f"""
            <div class="destination-card">
                <h2 style='color:#222;font-size:2rem;font-weight:800;margin-bottom:0.5rem;'>📍 {item.get('title', 'Untitled')}</h2>
            """, unsafe_allow_html=True)
            # Content'i daha görünür ve kontrastlı göster
            st.write(item.get('content', 'No content'))
            # Display labels
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
    with col2:
        if st.button("📂 Etiketlenmiş veriyle devam et", key="labeled_mode"):
            st.session_state['startup_mode'] = 'labeled'
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
    # List all .json files except output.json, changed.json, requirements.txt, etc.
    exclude = {"output.json", "changed.json", "requirements.txt", "README.md", "README_rules.md", ".cursorrules"}
    json_files = [f for f in glob.glob("*.json") if os.path.basename(f) not in exclude]
    if not json_files:
        st.warning("Kök dizinde hiç etiketlenmiş veri dosyası bulunamadı.")
        st.stop()
    default_file = "labeled_output.json" if "labeled_output.json" in json_files else json_files[0]
    selected_file = st.selectbox("Bir etiketlenmiş veri dosyası seçin:", json_files, index=json_files.index(default_file) if default_file in json_files else 0, key="labeled_file_select")
    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            labeled_data = json.load(f)
        display_labeled_data(labeled_data)
    except Exception as e:
        st.error(f"Seçilen dosya okunamadı: {str(e)}")
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
                    st.markdown("""
                    <div class="success-card">
                        <h4>✅ Labels generated successfully!</h4>
                        <p>Veriler kaydedilmeye hazır.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("### 💾 Bu dosyayı kaydetmek istediğiniz isim nedir?")
                    default_name = f"labeled_output_{int(time.time())}"
                    file_name = st.text_input("Dosya adı (uzantısız, ör: balat):", value="", key="save_filename")
                    if st.button("Kaydet", key="save_labeled_file"):
                        safe_name = file_name.strip() or default_name
                        if not safe_name.endswith(".json"):
                            safe_name += ".json"
                        with open(safe_name, "w", encoding="utf-8") as f:
                            json.dump(labeled_data, f, ensure_ascii=False, indent=2)
                        st.success(f"Etiketlenmiş veri {safe_name} olarak kaydedildi!")
                        st.session_state["last_labeled_file"] = safe_name
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
