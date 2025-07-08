# Project Purpose
This project is developed to fetch and analyze data from various websites. It provides a user-friendly experience with a Streamlit interface.

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd web_scraping
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create your `.env` file:
   Copy `.env.example` and enter your own API keys:
   ```bash
   cp .env.example .env
   ```

## .env Example
You should create a .env file like below:
```env
SCRAPINGBEE_API_KEY=your_scrapingbee_api_key
```

## Usage

```bash
streamlit run sbee_streamlit.py
```

## Required API Keys and Explanations
- `SCRAPINGBEE_API_KEY`: Required for web scraping operations with ScrapingBee service.

## Contribution
Please fork the repository and send a pull request to contribute. For questions or suggestions, you can open an issue.

## License
MIT License 