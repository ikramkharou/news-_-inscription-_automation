# Newsletter Subscription Automation

Automated newsletter subscription tool using Playwright. Supports multiple news websites with a centralized CLI interface.

## Setup

```bash
npm install
npx playwright install chromium
```

## Usage

## Exit Codes

- `0` - All URLs processed successfully
- `1` - At least one URL failed or invalid input

### Using Node.js --env flag (Recommended - Node.js 20+)

```bash
# Single URL
node --env:EMAIL=test@example.com --env:URL=https://www.foxnews.com/newsletters --env:HEADLESS=false main.js

# Multiple URLs (base64 encoded)
node --env:EMAIL=test@example.com --env:URLS="WyJodHRwczovL3d3dy5mb3huZXdzLmNvbS9uZXdzbGV0dGVycyIsImh0dHBzOi8vd3d3LnRoZWF0bGFudGljLmNvbS9uZXdzbGV0dGVycy8iXQ==" --env:HEADLESS=false main.js

# With proxy
node --env:EMAIL=test@example.com --env:URL=https://www.foxnews.com/newsletters --env:PROXY_URL=http://user:pass@host:port --env:HEADLESS=false main.js
```

### Using command line flags

```bash
# Single URL
node main.js --email test@example.com --url https://www.foxnews.com/newsletters --headless false

# Multiple URLs (base64 encoded)
node main.js --email test@example.com --urls "WyJodHRwczovL3d3dy5mb3huZXdzLmNvbS9uZXdzbGV0dGVycyIsImh0dHBzOi8vd3d3LnRoZWF0bGFudGljLmNvbS9uZXdzbGV0dGVycy8iXQ==" --headless false

# With proxy
node main.js --email test@example.com --url https://www.foxnews.com/newsletters --proxy http://user:pass@host:port --headless false
```

## Environment Variables

All arguments can also be provided as environment variables:

- `EMAIL` - Email address to subscribe
- `URL` or `SITE_URL` - Single URL to process
- `URLS` - Base64 encoded JSON array of URLs
- `HEADLESS` - Browser headless mode (true/false, default: true)
- `PROXY_URL` - Proxy URL (format: http://user:pass@host:port)

## Encoding URLs for Batch Processing

Use the `encode-urls.js` utility to encode a JSON array of URLs:

```bash
# Create a JSON file with URLs
echo '["https://www.foxnews.com/newsletters", "https://www.theatlantic.com/newsletters/"]' > urls.json

# Encode to base64
node encode-urls.js urls.json

# Copy the base64 string and use it with --urls or URLS env variable
```

Or pipe directly:

```bash
echo '["https://www.foxnews.com/newsletters"]' | node encode-urls.js
```

## Supported Websites

- **Fox News** - `https://www.foxnews.com/newsletters`
- **The Atlantic** - `https://www.theatlantic.com/newsletters/`
- **CNN** - `https://edition.cnn.com/newsletters`
- **The Verge** - `https://www.theverge.com/newsletters`
- **Vox** - `https://www.vox.com/newsletters`
- **AP News** - `https://apnews.com/newsletters`
- **National Review** - `https://link.nationalreview.com/join/4rc/newdesign-nls-signup`
- **Axios** - `https://www.axios.com/newsletters`
- **PennLive** - `https://link.pennlive.com/join/6fl/signup`
- **The Guardian** - `https://www.theguardian.com/email-newsletters`
- **TechCrunch** - `https://techcrunch.com/newsletters/`
- **Quartz** - `https://qz.com/newsletter`

## Features

- **Single Browser Session**: When processing multiple URLs, uses one browser instance and reuses the same tab
- **Proxy Support**: Configure proxy via `--proxy` or `PROXY_URL` environment variable
- **Exit Codes**: Returns `0` for success, `1` for failure
- **Batch Processing**: Process multiple URLs from a base64 encoded JSON array
- **Error Handling**: Continues processing remaining URLs even if one fails


```

## Notes

- The browser will reuse the same tab when processing multiple URLs
- If a page crashes or closes, a new page is created automatically for remaining URLs
- All scrapers throw errors on failure, which are caught and reported by `main.js`
- The tool processes URLs sequentially within a single browser session
