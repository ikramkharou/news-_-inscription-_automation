# Newsletter Subscription Automation

A modular Python application for automating newsletter subscriptions across multiple news websites using Playwright.

## Features

- Modular architecture with separate scraper classes for each website
- Command-line interface (CLI) for easy automation
- Automatic proxy rotation support
- Support for multiple news websites
- Clean, maintainable code structure
- Headless and visible browser modes

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
│   └── [website]_scraper.py
├── core/                   # Core base classes
│   └── base_scraper.py     # Base scraper class
├── email/                  # Email processing and validation
│   ├── processor.py        # Email processing service
│   └── validator.py         # Email validation utilities
├── factory/                # Factory pattern for scraper creation
│   └── scraper_factory.py
├── config.py               # Configuration constants
├── main.py                 # Application entry point (CLI)
└── app.py                  # FastAPI REST API server
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ikramkharou/news-_-inscription-_automation.git
cd news-_-inscription-_automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Configure proxies (optional):
   - Create a proxy file with format: `IP:PORT:USERNAME:PASSWORD`
   - Update `PROXY_FILE` in `config.py` if using a different filename

## Usage

### Command Line Interface (CLI) - `main.py`

For command-line usage, use `main.py`. The application runs from the command line with the following arguments:

```bash
python main.py --email <email> --url <url> --headless <true|false>
```

### Arguments

- `--email`: Email address(es) to subscribe (can be single email or comma-separated list)
- `--url`: Website URL to subscribe to
- `--headless`: Run browser in headless mode (`true` or `false`). Default: `false`

### Examples

**Single email with headless mode:**
```bash
python main.py --email test@example.com --url https://www.vox.com/newsletters --headless true
```

**Single email with visible browser:**
```bash
python main.py --email test@example.com --url https://www.cnn.com/newsletters --headless false
```

**Multiple emails (comma-separated):**
```bash
python main.py --email email1@test.com,email2@test.com --url https://www.vox.com/newsletters --headless true
```




#### CORS Configuration

The API is configured with CORS middleware to allow frontend integration. By default, it allows all origins. For production, update the `allow_origins` in `app.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### How It Works

1. The application detects the website from the URL
2. Uses the appropriate scraper class from the factory
3. Processes each email address sequentially
4. Handles subscriptions automatically with human-like delays
5. Logs all results to the console

## Configuration

Edit `config.py` to customize:

- `PROXY_FILE`: Path to proxy file
- `DEFAULT_HEADLESS`: Browser headless mode (True/False)
- `BROWSER_TIMEOUT`: Timeout for browser operations in milliseconds
- `EMAIL_PROCESSING_DELAY`: Delay between email processing in seconds
- `SUPPORTED_SITES`: Dictionary of supported websites and their domains

## Architecture

### Core Module
The `core/` folder contains base classes:
- `BaseScraper`: Provides proxy management, browser launch, and common email processing workflow

### Email Module
The `email/` folder contains:
- `EmailProcessor`: Handles the business logic for processing multiple emails
- `EmailValidator`: Provides email validation and parsing utilities

### Factory Pattern
`ScraperFactory` automatically selects the correct scraper class based on the URL provided.

### Scraper Classes
Each website has its own scraper class in `Class_Newsletters/` that inherits from `BaseScraper` and implements site-specific subscription logic.

## Adding New Websites

1. Create a new scraper class in `Class_Newsletters/`:
```python
from core.base_scraper import BaseScraper
from playwright.async_api import Page

class NewWebsiteScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://example.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        # Implement subscription logic
        # Use page.locator(), page.get_by_role(), etc.
        # Add delays with page.wait_for_timeout() for human-like behavior
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
- fastapi
- uvicorn
- pydantic

All dependencies are listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

## Output

The application provides detailed logging output showing:
- Processing status for each email
- Success/failure counts
- Error messages if any failures occur
- Final summary with total, success, and failed counts

## License

This project is provided as-is for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Notes

- Proxy file is gitignored for security
- Browser runs in visible mode by default (use `--headless true` for headless)
- Each scraper implements site-specific subscription logic with human-like delays
- Logging is configured for debugging and monitoring
- All output uses logger instead of print statements
