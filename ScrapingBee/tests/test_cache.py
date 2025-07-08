import os
import tempfile
from scrapingbee_cache import get_html

def test_get_html_cache():
    url = "https://www.example.com/"
    # First call should save to cache
    html1 = get_html(url)
    assert isinstance(html1, str) and len(html1) > 0
    # Second call should read from cache
    html2 = get_html(url)
    assert html1 == html2 