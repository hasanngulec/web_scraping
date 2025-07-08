import streamlit as st   # streamlit run sbee_streamlit.py
from ScrapingBee.scrapingbee_cache import get_html
from bs4 import BeautifulSoup
import json

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

st.title("Web Scraper and Parser with ScrapingBee")

url = st.text_input("Enter a URL:")

# Data and selections will be stored in session_state
if "places" not in st.session_state:
    st.session_state["places"] = []
if "remove_indices" not in st.session_state:
    st.session_state["remove_indices"] = []

if st.button("Fetch and Parse Data"):
    with st.spinner("Fetching and processing data..."):
        html = get_html(url)
        st.session_state["places"] = parse_destinations(html)
        st.session_state["remove_indices"] = []  # Reset selections on each fetch
        # Save original data as output.json
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state["places"], f, ensure_ascii=False, indent=2)

places = st.session_state["places"]

if places:
    st.success(f"{len(places)} destinations found!")
    titles = [f"{i}: {item['title']}" for i, item in enumerate(places)]
    remove_indices = st.multiselect(
        "Select the titles you do NOT want to keep:",
        options=list(range(len(places))),
        format_func=lambda i: titles[i],
        key="remove_indices"
    )
    filtered_places = [item for i, item in enumerate(places) if i not in remove_indices]
    st.write(f"{len(filtered_places)} titles remaining:")
    st.json(filtered_places)

    # Save as changed.json button
    if st.button("Save remaining as changed.json"):
        with open("changed.json", "w", encoding="utf-8") as f:
            json.dump(filtered_places, f, ensure_ascii=False, indent=2)
        st.success("changed.json file saved!")
