import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class QuartzScraper extends BaseScraper {
    getUrl() {
        return "https://qz.com/newsletter";
    }

    async subscribeEmail(page, email) {
        try {
            await page.pause();
            logger.info(`Starting subscription for ${email} to Quartz`);
            
            // Click and fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Enter email here" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await emailInput.click();
                await emailInput.fill(email);
                await page.waitForTimeout(1000);
                logger.info(`Filled email address field for ${email}`);
            } catch (error) {
                logger.error(`Error filling email address for ${email}: ${error.message}`);
                throw error;
            }
            
            // Wait for "Sign me up" button and click it
            try {
                const signupButton = page.getByRole("button", { name: "Sign me up" });
                await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                
                await signupButton.scrollIntoViewIfNeeded();
                await page.waitForTimeout(500);
                
                await signupButton.click();
                logger.info(`Clicked Sign me up button for ${email}`);
                await page.waitForTimeout(3000);
                logger.info(`Waiting for confirmation message for ${email}`);
            } catch (error) {
                logger.error(`Error clicking Sign me up button for ${email}: ${error.message}`);
                throw error;
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to Quartz newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to Quartz: ${error.message}`);
            throw error;
        }
    }
}

