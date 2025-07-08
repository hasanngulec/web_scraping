# scrapingbee_cache

A simple Python library to fetch web pages with caching using ScrapingBee.

## Installation

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Add your ScrapingBee API key to your .env file:
   ```env
   SCRAPINGBEE_API_KEY=your_scrapingbee_api_key
   ```

## Usage

```python
from scrapingbee_cache import get_html

html = get_html("https://www.example.com/")
print(html[:200])
```

- On the first call, the page is fetched using ScrapingBee and saved to the `cache/` directory.
- On subsequent calls, the page is read from the cache without consuming your API quota.

## Testing

```bash
pytest tests/
```

## Contributing
To contribute, fork the repository and submit a pull request.

## License
MIT License 