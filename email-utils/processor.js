import { chromium } from 'playwright';
import { logger, EMAIL_PROCESSING_DELAY } from '../config.js';
import { ScraperFactory } from '../factory/scraper-factory.js';

export class EmailProcessor {
    constructor() {
        this.scraperFactory = ScraperFactory;
    }

    async processEmails(url, emails, headless = false) {
        const results = {
            total: emails.length,
            success: 0,
            failed: 0,
            errors: []
        };
        
        const ScraperClass = this.scraperFactory.getScraperClass(url);
        if (!ScraperClass) {
            const errorMsg = `Unsupported website URL: ${url}`;
            results.errors.push(errorMsg);
            logger.error(errorMsg);
            return results;
        }
        
        try {
            const scraper = new ScraperClass();
            const playwright = { chromium };
            
            for (const email of emails) {
                try {
                    await scraper.processEmail(email, playwright, headless);
                    results.success += 1;
                    
                    // Wait between email processing
                    if (EMAIL_PROCESSING_DELAY > 0) {
                        await new Promise(resolve => setTimeout(resolve, EMAIL_PROCESSING_DELAY * 1000));
                    }
                } catch (error) {
                    results.failed += 1;
                    const errorMsg = `Failed to process ${email}: ${error.message}`;
                    results.errors.push(errorMsg);
                    logger.error(errorMsg);
                }
            }
        } catch (error) {
            logger.error(`Error in processEmails: ${error.message}`);
            throw error;
        }
        
        logger.info(`Processing complete: ${results.success} success, ${results.failed} failed`);
        return results;
    }
}

