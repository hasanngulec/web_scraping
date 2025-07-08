import os
from dotenv import load_dotenv
import requests
from .utils import url_to_filename

# Load .env file (only runs on first import)
load_dotenv()

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def get_html(url: str) -> str:
    """
    Returns the HTML content of the given URL with caching.
    - First, it checks the cache. If present, reads from there.
    - If not, fetches using ScrapingBee, saves to cache.
    """
    cache_path = os.path.join(CACHE_DIR, url_to_filename(url))
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()
    api_key = os.getenv("SCRAPINGBEE_KEY")
    if not api_key:
        raise RuntimeError("SCRAPINGBEE_KEY not found! Please check your .env file.")
    response = requests.get(
        "https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": api_key,
            "url": url,
            "render_js": "false"
        },
        timeout=15
    )
    response.raise_for_status()
    html = response.text
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html 