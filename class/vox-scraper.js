import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class VoxScraper extends BaseScraper {
    getUrl() {
        return "https://www.vox.com/newsletters";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to Vox`);
            
            // Click labels in start-here section
            try {
                await page.locator("#start-here label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#start-here label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#start-here label").nth(1).click();
                await page.waitForTimeout(3000);
                await page.locator("#start-here label").nth(2).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked start-here labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking start-here labels for ${email}: ${error.message}`);
            }
            
            // Click labels in politics-and-policy section
            try {
                await page.locator("#politics-and-policy label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#politics-and-policy label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#politics-and-policy label").nth(1).click();
                await page.waitForTimeout(3000);
                await page.locator("#politics-and-policy label").nth(2).click();
                await page.waitForTimeout(3000);
                await page.locator("#politics-and-policy label").nth(3).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked politics-and-policy labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking politics-and-policy labels for ${email}: ${error.message}`);
            }
            
            // Click labels in future-perfect section
            try {
                await page.locator("#future-perfect label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#future-perfect label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#future-perfect label").nth(1).click();
                await page.waitForTimeout(3000);
                await page.locator("#future-perfect label").nth(2).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked future-perfect labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking future-perfect labels for ${email}: ${error.message}`);
            }
            
            // Click labels in culture-and-technology section
            try {
                await page.locator("#culture-and-technology label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#culture-and-technology label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#culture-and-technology label").nth(1).click();
                await page.waitForTimeout(3000);
                await page.locator("#culture-and-technology label").nth(2).click();
                await page.waitForTimeout(3000);
                await page.locator("#culture-and-technology label").nth(3).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked culture-and-technology labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking culture-and-technology labels for ${email}: ${error.message}`);
            }
            
            // Click labels in build-new-habits section
            try {
                await page.locator("#build-new-habits label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#build-new-habits label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#build-new-habits label").nth(1).click();
                await page.waitForTimeout(3000);
                await page.locator("#build-new-habits label").nth(2).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked build-new-habits labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking build-new-habits labels for ${email}: ${error.message}`);
            }
            
            // Click labels in just-for-fun section
            try {
                await page.locator("#just-for-fun label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.locator("#just-for-fun label").first().click();
                await page.waitForTimeout(3000);
                await page.locator("#just-for-fun label").nth(1).click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked just-for-fun labels for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking just-for-fun labels for ${email}: ${error.message}`);
            }
            
            // Fill email address
            try {
                const emailInput = page.locator("#email");
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
                const signupButton = page.locator('xpath=//*[@id="content"]/div[1]/div/div/form/div/div[2]/fieldset/div/button');
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
            logger.info(`Subscribed ${email} to Vox newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to Vox: ${error.message}`);
            throw error;
        }
    }
}

