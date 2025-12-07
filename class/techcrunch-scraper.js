import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class TechCrunchScraper extends BaseScraper {
    getUrl() {
        return "https://techcrunch.com/newsletters/";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to TechCrunch`);
            
            // Click "Select All" button
            try {
                const selectAllButton = page.getByRole("button", { name: "Select All", exact: true });
                await selectAllButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await selectAllButton.click();
                await page.waitForTimeout(1000);
                logger.info(`Clicked Select All button for ${email}`);
            } catch (error) {
                logger.error(`Error clicking Select All button for ${email}: ${error.message}`);
                throw error;
            }
            
            // Fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Email address" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await emailInput.click();
                await page.waitForTimeout(1000);
                await emailInput.fill(email);
                await page.waitForTimeout(1000);
                logger.info(`Filled email address field for ${email}`);
            } catch (error) {
                logger.error(`Error filling email address for ${email}: ${error.message}`);
                throw error;
            }
            
            // Click Subscribe button
            try {
                const subscribeButton = page.locator('xpath=/html/body/div[3]/main/div/form/div/div[3]/div/div/div[2]/fieldset/div[2]/div/div/div/button');
                await subscribeButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                
                await subscribeButton.scrollIntoViewIfNeeded();
                await page.waitForTimeout(1000);
                
                for (let clickNumber = 0; clickNumber < 2; clickNumber++) {
                    try {
                        const box = await subscribeButton.boundingBox();
                        if (box) {
                            await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
                            await page.waitForTimeout(200);
                        }
                        
                        await subscribeButton.click({ timeout: 5000, delay: 100 });
                        logger.info(`Clicked Subscribe button ${clickNumber + 1} (human-like click) for ${email}`);
                    } catch (clickError) {
                        if (clickError.message.toLowerCase().includes("intercepts") || clickError.message.toLowerCase().includes("intercepted")) {
                            logger.warn(`Click intercepted, trying force click for ${email}`);
                            await subscribeButton.click({ force: true, delay: 100 });
                            logger.info(`Clicked Subscribe button ${clickNumber + 1} (force click) for ${email}`);
                        } else {
                            logger.warn(`Regular click failed, trying JavaScript click for ${email}`);
                            await subscribeButton.evaluate(element => element.click());
                            logger.info(`Clicked Subscribe button ${clickNumber + 1} (JavaScript click) for ${email}`);
                        }
                    }
                    
                    if (clickNumber < 1) {
                        await page.waitForTimeout(500);
                    }
                }
                
                await page.waitForTimeout(3000);
                logger.info(`Waiting for confirmation message for ${email}`);
            } catch (error) {
                logger.error(`Error clicking Subscribe button for ${email}: ${error.message}`);
                throw error;
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to TechCrunch newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to TechCrunch: ${error.message}`);
            throw error;
        }
    }
}

