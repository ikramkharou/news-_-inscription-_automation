# Newsletter Subscription Automation

A modular Python application for automating newsletter subscriptions across multiple news websites using Playwright.

## Features

- Modular architecture with separate scraper classes for each website
- Tkinter-based GUI for easy email and URL input
- Automatic proxy rotation support
- Support for multiple news websites
- Clean, maintainable code structure

## Supported Websites

- CNN
- Fox News
- The Atlantic
- The Verge
- Vox
- AP News
- National Review
- Axios
- PennLive
- The Guardian
- TechCrunch
- Quartz

## Project Structure

```
News_inscrip/
├── Class_Newsletters/      # Scraper classes for each website
│   ├── base_scraper.py     # Base scraper class
│   └── [website]_scraper.py
├── factory/                # Factory pattern for scraper creation
│   └── scraper_factory.py
├── services/               # Business logic layer
│   └── email_processor.py
├── gui/                    # User interface
│   └── newsletter_app.py
├── utils/                  # Utility functions
│   └── email_validator.py
├── config.py               # Configuration constants
└── main.py                 # Application entry point
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ikramkharou/news-_-inscription-_automation.git
cd news-_-inscription-_automation
```

2. Install dependencies:
```bash
pip install playwright
playwright install chromium
```

3. Configure proxies (optional):
   - Create a proxy file with format: `IP:PORT:USERNAME:PASSWORD`
   - Update `PROXY_FILE` in `config.py` if using a different filename

## Usage

1. Run the application:
```bash
python main.py
```

2. In the GUI:
   - Enter the website URL in the URL field
   - Enter email addresses (one per line) in the email list text area
   - Click "Start Subscription" to begin

3. The application will:
   - Detect the website from the URL
   - Use the appropriate scraper class
   - Process each email address
   - Handle subscriptions automatically

## Configuration

Edit `config.py` to customize:

- `PROXY_FILE`: Path to proxy file
- `DEFAULT_HEADLESS`: Browser headless mode (True/False)
- `BROWSER_TIMEOUT`: Timeout for browser operations in milliseconds
- `EMAIL_PROCESSING_DELAY`: Delay between email processing in seconds
- `SUPPORTED_SITES`: Dictionary of supported websites and their domains

## Architecture

### Base Scraper
All scraper classes inherit from `BaseScraper` which provides:
- Proxy management
- Browser launch and management
- Common email processing workflow

### Factory Pattern
`ScraperFactory` automatically selects the correct scraper class based on the URL provided.

### Service Layer
`EmailProcessor` handles the business logic for processing multiple emails.

### GUI Layer
`NewsletterApp` provides a Tkinter-based interface for user interaction.

## Adding New Websites

1. Create a new scraper class in `Class_Newsletters/`:
```python
from .base_scraper import BaseScraper
from playwright.async_api import Page

class NewWebsiteScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://example.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        # Implement subscription logic
        pass
```

2. Update `config.py`:
```python
SUPPORTED_SITES = {
    # ... existing sites
    "New Website": ["example.com"]
}
```

3. Update `factory/scraper_factory.py`:
```python
from Class_Newsletters.newwebsite_scraper import NewWebsiteScraper

_scraper_map = {
    # ... existing scrapers
    "New Website": NewWebsiteScraper
}
```

4. Update `Class_Newsletters/__init__.py` to export the new class

## Requirements

- Python 3.7+
- playwright
- tkinter (usually included with Python)

## License

This project is provided as-is for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Notes

- Proxy file is gitignored for security
- Browser runs in visible mode by default for debugging
- Each scraper implements site-specific subscription logic
- Logging is configured for debugging and monitoring

