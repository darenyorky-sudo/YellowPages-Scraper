# YellowPages Scraper

A robust web scraper built with Playwright to extract business information (Name, Phone, Website) from YellowPages.

## Features
- Stateless scraping: Opens a fresh session per page to bypass anti-bot protections.
- Randomized delays to mimic human behavior.
- Configuration-driven: Easily change search terms or location in `config.py`.

## Setup
1. Install dependencies: `pip install playwright`
2. Install browsers: `python -m playwright install`
3. Run the script: `python scraper/main.py`