from setuptools import setup, find_packages

setup(
    name="scrapingbee_cache",
    version="0.1.0",
    description="A Python library for web scraping with ScrapingBee and caching support",
    author="Your name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    python_requires=">=3.7",
) 