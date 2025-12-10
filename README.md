# Newsletter Subscription Automation (CLI)

Minimal desktop/CLI tool to subscribe emails to supported news sites using Playwright.

## Setup
```bash
npm install
npx playwright install chromium
```

## Run
Use flags or env vars (flags win):
```bash
# with flags
node main.js --email test@example.com --url https://www.vox.com/newsletters --headless true

# with env file (Node 20+)
node --env-file=.env main.js
```

Example `.env`:
```
EMAILS=test@example.com
URL=https://www.vox.com/newsletters
HEADLESS=true
PROXY_URL=
PROXY_FILE=250 proxies (1).txt
EMAIL_PROCESSING_DELAY=2
BROWSER_TIMEOUT=10000
```

## Supported sites
CNN, Fox News, The Atlantic, The Verge, Vox, AP News, National Review, Axios, PennLive, The Guardian, TechCrunch, Quartz.

## Notes
- HEADLESS defaults from `config.js` if unset.
- URLs must match a supported domain; otherwise the run exits as unsupported.
- PROXY_URL (e.g., `http://user:pass@host:port`) or PROXY_FILE can be used for proxying.

