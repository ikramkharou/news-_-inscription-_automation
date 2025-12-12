import { chromium } from 'playwright';
import { subscribeEmail as pennliveSubscribe } from './class/pennlive-scraper.js';
import { subscribeEmail as foxSubscribe } from './class/fox-scraper.js';
import { subscribeEmail as theatlanticSubscribe } from './class/theatlantic-scraper.js';
import { subscribeEmail as nationalreviewSubscribe } from './class/nationalreview-scraper.js';
import { subscribeEmail as apnewsSubscribe } from './class/apnews-scraper.js';
import { subscribeEmail as cnnSubscribe } from './class/cnn-scraper.js';
import { subscribeEmail as thevergeSubscribe } from './class/theverge-scraper.js';
import { subscribeEmail as voxSubscribe } from './class/vox-scraper.js';
import { subscribeEmail as theguardianSubscribe } from './class/theguardian-scraper.js';
import { subscribeEmail as techcrunchSubscribe } from './class/techcrunch-scraper.js';
import { subscribeEmail as quartzSubscribe } from './class/quartz-scraper.js';
import { subscribeEmail as axiosSubscribe } from './class/axios-scraper.js';

// URL to scraper mapping
const SCRAPER_MAP = {
    'pennlive.com': { fn: pennliveSubscribe, defaultUrl: 'https://link.pennlive.com/join/6fl/signup' },
    'foxnews.com': { fn: foxSubscribe, defaultUrl: 'https://www.foxnews.com/newsletters' },
    'fox.com': { fn: foxSubscribe, defaultUrl: 'https://www.foxnews.com/newsletters' },
    'theatlantic.com': { fn: theatlanticSubscribe, defaultUrl: 'https://www.theatlantic.com/newsletters/' },
    'nationalreview.com': { fn: nationalreviewSubscribe, defaultUrl: 'https://link.nationalreview.com/join/4rc/newdesign-nls-signup' },
    'apnews.com': { fn: apnewsSubscribe, defaultUrl: 'https://apnews.com/newsletters' },
    'cnn.com': { fn: cnnSubscribe, defaultUrl: 'https://edition.cnn.com/newsletters' },
    'edition.cnn.com': { fn: cnnSubscribe, defaultUrl: 'https://edition.cnn.com/newsletters' },
    'theverge.com': { fn: thevergeSubscribe, defaultUrl: 'https://www.theverge.com/newsletters' },
    'vox.com': { fn: voxSubscribe, defaultUrl: 'https://www.vox.com/newsletters' },
    'theguardian.com': { fn: theguardianSubscribe, defaultUrl: 'https://www.theguardian.com/email-newsletters' },
    'techcrunch.com': { fn: techcrunchSubscribe, defaultUrl: 'https://techcrunch.com/newsletters/' },
    'qz.com': { fn: quartzSubscribe, defaultUrl: 'https://qz.com/newsletter' },
    'axios.com': { fn: axiosSubscribe, defaultUrl: 'https://www.axios.com/newsletters' }
};

function parseBool(value, fallback = false) {
    if (value === undefined || value === null) return fallback;
    const normalized = value.toString().trim().toLowerCase();
    return ["1", "true", "yes", "y"].includes(normalized);
}

function parseEnvArgs(argv = process.argv.slice(2)) {
    // Parse --envVARIABLE=value arguments and set them as environment variables
    const envArgs = argv.filter(arg => arg.startsWith("--env"));
    envArgs.forEach(arg => {
        const envMatch = arg.match(/^--env(.+?)=(.*)$/);
        if (envMatch) {
            process.env[envMatch[1]] = envMatch[2];
        }
    });
}

function getScraperForUrl(url) {
    try {
        const urlObj = new URL(url);
        const hostname = urlObj.hostname.replace('www.', '');
        
        // Try exact match first
        if (SCRAPER_MAP[hostname]) {
            return SCRAPER_MAP[hostname];
        }
        
        // Try partial match
        for (const [key, value] of Object.entries(SCRAPER_MAP)) {
            if (hostname.includes(key) || key.includes(hostname)) {
                return value;
            }
        }
        
        return null;
    } catch (error) {
        return null;
    }
}

function getProxy(proxyUrl) {
    if (proxyUrl) {
        return { server: proxyUrl };
    }
    return null;
}

function decodeBase64Urls(base64String) {
    try {
        const decoded = Buffer.from(base64String, 'base64').toString('utf-8');
        const urls = JSON.parse(decoded);
        if (Array.isArray(urls)) {
            return urls;
        }
        console.error("Decoded string is not an array of URLs");
        return [];
    } catch (error) {
        console.error(`Error decoding base64 URLs: ${error.message}`);
        return [];
    }
}

async function processUrls(urls, email, headless, proxy) {
    if (!Array.isArray(urls) || urls.length === 0) {
        return [];
    }

    const results = [];
    const launchOptions = { headless };
    if (proxy) {
        launchOptions.proxy = proxy;
    }

    let browser = null;
    let context = null;
    let page = null;

    try {
        console.log(`Launching browser once (headless=${headless}${proxy ? `, proxy=${proxy.server}` : ''})`);
        browser = await chromium.launch(launchOptions);
        context = await browser.newContext();
        context.setDefaultNavigationTimeout(10_000);
        context.setDefaultTimeout(10_000);
        page = await context.newPage();

        for (const url of urls) {
            const scraper = getScraperForUrl(url);
            if (!scraper) {
                console.error(`Unsupported website URL: ${url}`);
                results.push({ success: false, url, error: 'Unsupported URL' });
                continue;
            }

            const finalUrl = url || scraper.defaultUrl;
            try {
                console.log(`\n[${url}] Navigating to ${finalUrl}`);
                await page.goto(finalUrl);
                await scraper.fn(page, email);
                console.log(`[${url}] Successfully subscribed ${email}`);
                results.push({ success: true, url });
            } catch (error) {
                console.error(`[${url}] Fatal error: ${error.message}`);
                // If the page was closed or crashed, recreate it for next URLs
                if (page && page.isClosed && page.isClosed()) {
                    page = await context.newPage();
                }
                results.push({ success: false, url, error: error.message });
            }
        }
    } catch (error) {
        console.error(`Browser-level fatal error: ${error.message}`);
        return urls.map(url => ({ success: false, url, error: error.message }));
    } finally {
        if (browser) {
            await browser.close();
        }
    }

    return results;
}

async function main() {
    parseEnvArgs();
    
    const email = process.env.EMAIL;
    const url = process.env.URL || process.env.SITE_URL;
    const urlsBase64 = process.env.URLS;
    const headless = parseBool(process.env.HEADLESS, true);
    const proxyUrl = process.env.PROXY_URL || process.env.PROXY;

    if (!email) {
        console.error("No email provided. Use --email or EMAIL env variable.");
        process.exit(1);
    }

    // Get proxy if provided
    const proxy = getProxy(proxyUrl);
    
    if (proxy) {
        console.log(`Using proxy: ${proxy.server}`);
    }

    // Build URL list: prefer base64 list, fallback to single URL
    let urls = [];
    if (urlsBase64) {
        console.log("Decoding base64 URLs...");
        urls = decodeBase64Urls(urlsBase64);
        if (urls.length === 0) {
            console.error("No valid URLs found in base64 string.");
            process.exit(1);
        }
    } else if (url) {
        urls = [url];
    } else {
        console.error("No URL provided. Use --url, --urls (base64), or URL/SITE_URL env variable.");
        process.exit(1);
    }

    console.log(`Processing ${urls.length} URL(s) with a single browser session...`);
    const results = await processUrls(urls, email, headless, proxy);

    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;

    console.log("\n" + "=".repeat(50));
    console.log("PROCESSING RESULTS");
    console.log("=".repeat(50));
    console.log(`Total URLs: ${results.length}`);
    console.log(`Success: ${successCount}`);
    console.log(`Failed: ${failCount}`);

    if (failCount > 0) {
        console.log("\nFailed URLs:");
        results.filter(r => !r.success).forEach(r => {
            console.log(`  - ${r.url}: ${r.error}`);
        });
    }

    process.exit(failCount > 0 ? 1 : 0);
}

main();
