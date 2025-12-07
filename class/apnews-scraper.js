import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class APNewsScraper extends BaseScraper {
    getUrl() {
        return "https://apnews.com/newsletters";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to AP News`);
            
            // Step 1: Click checkbox labels
            const checkboxSelectors = [
                ".checkbox-label", // first
                "div:nth-child(2) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(3) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(4) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(5) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(6) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
            ];
            
            for (const selector of checkboxSelectors) {
                try {
                    const checkbox = selector === ".checkbox-label" 
                        ? page.locator(selector).first()
                        : page.locator(selector);
                    
                    await checkbox.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                    await checkbox.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(300);
                    await checkbox.click();
                    await page.waitForTimeout(1000);
                    logger.info(`Clicked checkbox ${selector} for ${email}`);
                } catch (error) {
                    logger.warn(`Error clicking checkbox ${selector} for ${email}: ${error.message}`);
                    continue;
                }
            }
            
            // Step 2: Click SELECT buttons multiple times
            for (let i = 0; i < 3; i++) {
                try {
                    const selectButton = page.getByText("SELECT", { exact: true }).first();
                    await selectButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                    await page.waitForTimeout(500);
                    await selectButton.click();
                    await page.waitForTimeout(1000);
                    logger.info(`Clicked SELECT button (first) - click ${i+1} for ${email}`);
                } catch (error) {
                    logger.warn(`Error clicking SELECT button (first) - click ${i+1} for ${email}: ${error.message}`);
                }
            }
            
            // Click "Enable accessibility" text
            try {
                const enableAccessibility = page.getByText("Enable accessibility0 .st0{");
                await enableAccessibility.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(500);
                await enableAccessibility.click();
                await page.waitForTimeout(1000);
                logger.info(`Clicked Enable accessibility for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking Enable accessibility for ${email}: ${error.message}`);
            }
            
            // Click SELECT button first one more time
            try {
                const selectButton = page.getByText("SELECT", { exact: true }).first();
                await selectButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(500);
                await selectButton.click();
                await page.waitForTimeout(1000);
                logger.info(`Clicked SELECT button (first) again for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking SELECT button (first) again for ${email}: ${error.message}`);
            }
            
            // Click SELECT button without .first
            try {
                const selectButton = page.getByText("SELECT", { exact: true });
                await selectButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(500);
                await selectButton.click();
                await page.waitForTimeout(1000);
                logger.info(`Clicked SELECT button (no first) for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking SELECT button (no first) for ${email}: ${error.message}`);
            }
            
            // Step 3: Fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Share your email here" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                
                await emailInput.click();
                await page.waitForTimeout(500);
                
                // Clear any existing content
                await emailInput.press("Control+a");
                await page.waitForTimeout(200);
                await emailInput.press("Delete");
                await page.waitForTimeout(300);
                
                const cleanEmail = email.trim();
                await emailInput.fill(cleanEmail);
                await page.waitForTimeout(500);
                
                // Press Tab to trigger email validation
                await emailInput.press("Tab");
                await page.waitForTimeout(2000);
                await page.waitForTimeout(1000);
                logger.info(`Filled email address field with clean email: ${cleanEmail}`);
            } catch (error) {
                logger.error(`Error filling email address for ${email}: ${error.message}`);
                throw error;
            }
            
            // Step 4: Click disclaimer checkbox
            try {
                const disclaimerCheckbox = page.getByRole("main").locator("div").filter({ hasText: "Newsletters Selected Please provide a valid email address, and check disclaimer" }).locator("label").nth(1);
                await disclaimerCheckbox.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await disclaimerCheckbox.scrollIntoViewIfNeeded();
                await page.waitForTimeout(500);
                await disclaimerCheckbox.click();
                await page.waitForTimeout(2000);
                logger.info(`Clicked disclaimer checkbox for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking disclaimer checkbox for ${email}: ${error.message}`);
            }
            
            // Step 5: Click submit button
            try {
                const submitButton = page.locator("#Newsletter-Banner-submitBtn");
                await submitButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(2000);
                await submitButton.scrollIntoViewIfNeeded();
                await page.waitForTimeout(500);
                await submitButton.click();
                logger.info(`Clicked submit button for ${email}`);
                await page.waitForTimeout(3000);
                logger.info(`Waiting for confirmation message for ${email}`);
            } catch (error) {
                logger.error(`Error clicking submit button for ${email}: ${error.message}`);
                throw error;
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to AP News newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to AP News: ${error.message}`);
            throw error;
        }
    }
}

