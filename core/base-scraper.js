import { readFileSync } from 'fs';
import { randomBytes } from 'crypto';
import { logger, PROXY_FILE, DEFAULT_HEADLESS, BROWSER_TIMEOUT } from '../config.js';

export class BaseScraper {
    constructor(proxyFile = PROXY_FILE) {
        this.proxyFile = proxyFile;
        this.proxies = this._loadProxies();
    }

    _loadProxies() {
        try {
            const proxies = [];
            const content = readFileSync(this.proxyFile, 'utf-8');
            const lines = content.split('\n');
            
            for (const line of lines) {
                const trimmed = line.trim();
                if (trimmed) {
                    const parts = trimmed.split(':');
                    if (parts.length === 4) {
                        const [ip, port, username, password] = parts;
                        proxies.push({
                            server: `http://${ip}:${port}`,
                            username,
                            password
                        });
                    }
                }
            }
            
            logger.info(`Loaded ${proxies.length} proxies`);
            return proxies;
        } catch (error) {
            logger.error(`Error loading proxies: ${error.message}`);
            return [];
        }
    }

    _getRandomProxy() {
        if (this.proxies.length > 0) {
            return this.proxies[Math.floor(Math.random() * this.proxies.length)];
        }
        return null;
    }

    async _launchBrowser(playwright, headless = DEFAULT_HEADLESS) {
            const chromium = playwright.chromium;
        const proxy = this._getRandomProxy();
        
        const launchOptions = { headless };
        if (proxy) {
            launchOptions.proxy = proxy;
            logger.info(`Launching browser with proxy: ${proxy.server} (headless=${headless})`);
        } else {
            logger.warn(`No proxy available, launching browser without proxy (headless=${headless})`);
        }
        
        const browser = await chromium.launch(launchOptions);
        logger.info("Browser launched successfully");
        return browser;
    }

    getUrl() {
        throw new Error("getUrl() method must be implemented by subclass");
    }

    async subscribeEmail(page, email) {
        throw new Error("subscribeEmail() method must be implemented by subclass");
    }

    async processEmail(email, playwright, headless = null) {
        let browser = null;
        try {
            if (headless === null) {
                headless = DEFAULT_HEADLESS;
            }
            

            const chromium = playwright.chromium;
            const proxy = this._getRandomProxy();
            
            const launchOptions = { headless };
            if (proxy) {
                launchOptions.proxy = proxy;
                logger.info(`Launching browser with proxy: ${proxy.server} (headless=${headless})`);
            } else {
                logger.warn(`No proxy available, launching browser without proxy (headless=${headless})`);
            }
            
            browser = await chromium.launch(launchOptions);
            logger.info("Browser launched successfully");
            
            const page = await browser.newPage();
            await page.goto(this.getUrl());
            
            await this.subscribeEmail(page, email);
            
            await browser.close();
            logger.info(`Successfully processed email: ${email}`);
        } catch (error) {
            logger.error(`Error processing email ${email}: ${error.message}`);
            if (browser) {
                await browser.close();
            }
            throw error;
        }
    }
}

