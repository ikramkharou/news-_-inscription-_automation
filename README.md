# Newsletter Subscription Automation

A modular Node.js application for automating newsletter subscriptions across multiple news websites using Playwright.

## Features

- Modular architecture with separate scraper classes for each website
- Command-line interface (CLI) for easy automation
- REST API for programmatic access
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
news-_-inscription-_automation/
├── class/                  # Scraper classes for each website
│   └── [website]-scraper.js
├── core/                   # Core base classes
│   └── base-scraper.js     # Base scraper class
├── email-utils/            # Email processing and validation
│   ├── processor.js        # Email processing service
│   └── validator.js        # Email validation utilities
├── factory/                # Factory pattern for scraper creation
│   └── scraper-factory.js
├── config.js               # Configuration constants
├── main.js                 # Application entry point (CLI)
├── app.js                  # Express REST API server
└── package.json            # Node.js dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ikramkharou/news-_-inscription-_automation.git
cd news-_-inscription-_automation
```

2. Install dependencies:
```bash
npm install
```

3. Install Playwright browsers:
```bash
npx playwright install chromium
```

4. Configure proxies (optional):
   - Create a proxy file with format: `IP:PORT:USERNAME:PASSWORD`
   - Update `PROXY_FILE` in `config.js` if using a different filename

## Usage

### Command Line Interface (CLI) - `main.js`

For command-line usage, use `main.js`. The application runs from the command line with the following arguments:

```bash
node main.js --email <email> --url <url> [--headless <true|false>]
```

### Arguments

- `--email, -e`: Email address(es) to subscribe (can be single email or comma-separated list)
- `--url, -u`: Website URL to subscribe to
- `--headless, -h`: Run browser in headless mode (`true` or `false`). Default: `false`

### Examples

**Single email with headless mode:**
```bash
node main.js --email test@example.com --url https://www.vox.com/newsletters --headless true
```

**Single email with visible browser:**
```bash
node main.js --email test@example.com --url https://www.cnn.com/newsletters --headless false
```

**Multiple emails (comma-separated):**
```bash
node main.js --email email1@test.com,email2@test.com --url https://www.vox.com/newsletters --headless true
```

### REST API - `app.js`

Start the API server:
```bash
npm run api
# or
node app.js
```


The API will run on `http://localhost:8000` by default.

#### API Endpoints

**Health Check:**
```bash
GET /health
```

**Get Supported Sites:**
```bash
GET /sites
```

**Subscribe to Newsletter:**
```bash
POST /subscribe
Content-Type: application/json

{
  "url": "https://www.vox.com/newsletters",
  "emails": ["test@example.com"],
  "headless": true
}
```

**Get Subscription Status:**
```bash
GET /subscribe/{task_id}
```

#### CORS Configuration

The API is configured with CORS middleware to allow frontend integration. By default, it allows all origins. For production, update the CORS configuration in `app.js`:

```javascript
app.use(cors({
    origin: ["https://yourfrontend.com"],  // Update this
    credentials: true,
    methods: ["*"],
    allowedHeaders: ["*"]
}));
```

### How It Works

1. The application detects the website from the URL
2. Uses the appropriate scraper class from the factory
3. Processes each email address sequentially
4. Handles subscriptions automatically with human-like delays
5. Logs all results to the console

## Configuration

Edit `config.js` to customize:

- `PROXY_FILE`: Path to proxy file
- `DEFAULT_HEADLESS`: Browser headless mode (true/false)
- `BROWSER_TIMEOUT`: Timeout for browser operations in milliseconds
- `EMAIL_PROCESSING_DELAY`: Delay between email processing in seconds
- `SUPPORTED_SITES`: Object of supported websites and their domains

## Architecture

### Core Module
The `core/` folder contains base classes:
- `BaseScraper`: Provides proxy management, browser launch, and common email processing workflow

### Email Module
The `email-utils/` folder contains:
- `EmailProcessor`: Handles the business logic for processing multiple emails
- `EmailValidator`: Provides email validation and parsing utilities

### Factory Pattern
`ScraperFactory` automatically selects the correct scraper class based on the URL provided.

### Scraper Classes
Each website has its own scraper class in `class/` that extends `BaseScraper` and implements site-specific subscription logic.

## Adding New Websites

1. Create a new scraper class in `class/`:
```javascript
import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class NewWebsiteScraper extends BaseScraper {
    getUrl() {
        return "https://example.com/newsletters";
    }

    async subscribeEmail(page, email) {
        // Implement subscription logic
        // Use page.locator(), page.getByRole(), etc.
        // Add delays with page.waitForTimeout() for human-like behavior
    }
}
```

2. Update `config.js`:
```javascript
export const SUPPORTED_SITES = {
    // ... existing sites
    "New Website": ["example.com"]
};
```

3. Update `factory/scraper-factory.js`:
```javascript
import { NewWebsiteScraper } from '../class/newwebsite-scraper.js';

// Add to _scraperMap
static _scraperMap = {
    // ... existing scrapers
    "New Website": NewWebsiteScraper
};
```

4. Export the new class from `class/newwebsite-scraper.js`

## Requirements

- Node.js 18.0.0 or higher
- npm or yarn package manager

## Dependencies

All dependencies are listed in `package.json`. Install with:
```bash
npm install
```

Key dependencies:
- `playwright`: Browser automation
- `express`: Web framework for REST API
- `zod`: Schema validation
- `commander`: CLI argument parsing
- `winston`: Logging
- `uuid`: Task ID generation

## Output

The application provides detailed logging output showing:
- Processing status for each email
- Success/failure counts
- Error messages if any failures occur
- Final summary with total, success, and failed counts

## Development

Run in development mode with auto-reload:

```bash
# CLI
npm run dev

# API
npm run api:dev
```

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
- All output uses logger instead of console statements
