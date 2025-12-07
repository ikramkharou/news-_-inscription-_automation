import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class TheVergeScraper extends BaseScraper {
    getUrl() {
        return "https://www.theverge.com/newsletters";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to The Verge`);
            
            // Click labels in free-newsletters section
            try {
                await page.locator("#free-newsletters label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#free-newsletters label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#free-newsletters label").nth(1).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked free-newsletters labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking free-newsletters labels for ${email}: ${error.message}`);
            }
            
            // Fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Enter your email" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await emailInput.click();
                await page.waitForTimeout(3000);
                await emailInput.fill(email);
                await page.waitForTimeout(3000);
                logger.info(`Filled email address field for ${email}`);
            } catch (error) {
                logger.error(`Error filling email address for ${email}: ${error.message}`);
                throw error;
            }
            
            // Click Sign Up button
            try {
                const signupButton = page.getByRole("button", { name: "Sign Up" });
                await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await signupButton.click();
                logger.info(`Clicked Sign Up button for ${email}`);
                await page.waitForTimeout(3000);
                logger.info(`Waiting for confirmation message for ${email}`);
            } catch (error) {
                logger.error(`Error clicking Sign Up button for ${email}: ${error.message}`);
                throw error;
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to The Verge newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to The Verge: ${error.message}`);
            throw error;
        }
    }
}

