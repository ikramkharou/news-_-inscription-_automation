import { logger, SUPPORTED_SITES } from '../config.js';
import { CNNScraper } from '../class/cnn-scraper.js';
import { FoxScraper } from '../class/fox-scraper.js';
import { TheAtlanticScraper } from '../class/theatlantic-scraper.js';
import { TheVergeScraper } from '../class/theverge-scraper.js';
import { VoxScraper } from '../class/vox-scraper.js';
import { APNewsScraper } from '../class/apnews-scraper.js';
import { NationalReviewScraper } from '../class/nationalreview-scraper.js';
import { AxiosScraper } from '../class/axios-scraper.js';
import { PennLiveScraper } from '../class/pennlive-scraper.js';
import { TheGuardianScraper } from '../class/theguardian-scraper.js';
import { TechCrunchScraper } from '../class/techcrunch-scraper.js';
import { QuartzScraper } from '../class/quartz-scraper.js';

export class ScraperFactory {
    static _scraperMap = {
        "CNN": CNNScraper,
        "Fox News": FoxScraper,
        "The Atlantic": TheAtlanticScraper,
        "The Verge": TheVergeScraper,
        "Vox": VoxScraper,
        "AP News": APNewsScraper,
        "National Review": NationalReviewScraper,
        "Axios": AxiosScraper,
        "PennLive": PennLiveScraper,
        "The Guardian": TheGuardianScraper,
        "TechCrunch": TechCrunchScraper,
        "Quartz": QuartzScraper
    };

    static createScraper(url) {
        const ScraperClass = this.getScraperClass(url);
        if (ScraperClass) {
            return new ScraperClass();
        }
        return null;
    }

    static getScraperClass(url) {
        if (!url) {
            return null;
        }
        
        const urlLower = url.toLowerCase().trim();
        
        for (const [siteName, domains] of Object.entries(SUPPORTED_SITES)) {
            for (const domain of domains) {
                if (urlLower.includes(domain)) {
                    const ScraperClass = this._scraperMap[siteName];
                    if (ScraperClass) {
                        logger.info(`Matched URL '${url}' to ${siteName} scraper`);
                        return ScraperClass;
                    }
                }
            }
        }
        
        logger.warn(`No scraper found for URL: ${url}`);
        return null;
    }

    static isSupportedUrl(url) {
        return this.getScraperClass(url) !== null;
    }

    static getSupportedSitesList() {
        return Object.keys(SUPPORTED_SITES).join(", ");
    }
}

