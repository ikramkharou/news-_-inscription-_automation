import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class FoxScraper extends BaseScraper {
    getUrl() {
        return "https://www.foxnews.com/newsletters";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to Fox`);
            
            // Step 1: Click first subscribe button
            try {
                const subscribeButton = page.locator(".button.subscribe > a").first();
                await subscribeButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await subscribeButton.click();
                await page.waitForTimeout(1000);
                logger.info(`Clicked first subscribe button for ${email}`);
            } catch (error) {
                logger.error(`Error clicking first subscribe button for ${email}: ${error.message}`);
                throw error;
            }
            
            // Step 2: Fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Type your email" });
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
            
            // Step 3: Click enter button
            try {
                const enterButton = page.locator(".button.enter > a").first();
                await enterButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await enterButton.click();
                await page.waitForTimeout(2000);
                logger.info(`Clicked enter button for ${email}`);
            } catch (error) {
                logger.error(`Error clicking enter button for ${email}: ${error.message}`);
                throw error;
            }
            
            // Step 4: Click all newsletter links
            const newsletterLinks = [
                ["Fox Business Breaking News", 2],
                ["Fox Business Breaking News", 3],
                ["Fox News First Get all the", 2],
                ["Fox News First Get all the", 3],
                ["Antisemitism Exposed Fox News", 2],
                ["Fox News Politics Get the", 2],
                ["Fox News Politics Get the", 3],
                ["Fox Business Rundown Get a", 2],
                ["Fox Business Rundown Get a", 3],
                ["Fox News Entertainment Get a", 2],
                ["Fox News Entertainment Get a", 3],
                ["Fox True Crime The hottest", 2],
                ["Best of Opinion Get the recap", 2],
                ["Best of Opinion Get the recap", 3],
                ["Fox News Lifestyle A look at", 2],
                ["Fox News Lifestyle A look at", 3],
                ["Fox News Health Stay up-to-", 2],
                ["Fox News Health Stay up-to-", 3],
                ["Fox News Sports Huddle", 2],
                ["Fox News Sports Huddle", 3],
            ];
            
            for (const [text, linkIndex] of newsletterLinks) {
                try {
                    const listitem = page.getByRole("listitem").filter({ hasText: text });
                    const link = listitem.getByRole("link").nth(linkIndex);
                    await link.waitFor({ state: 'visible', timeout: 5000 });
                    await link.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(300);
                    await link.click();
                    await page.waitForTimeout(1000);
                    logger.info(`Clicked newsletter link '${text}' nth(${linkIndex}) for ${email}`);
                } catch (error) {
                    logger.warn(`Error clicking newsletter link '${text}' nth(${linkIndex}) for ${email}: ${error.message}`);
                    continue;
                }
            }
            
            // Step 5: Click Subscribe links sequentially
            const subscribeLinkSequence = [1, 1, 1, 1, 2, 3, 1];
            
            for (const nthIndex of subscribeLinkSequence) {
                try {
                    const subscribeLink = page.getByRole("link", { name: "Subscribe" }).nth(nthIndex);
                    await subscribeLink.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                    await page.waitForTimeout(500);
                    await subscribeLink.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(300);
                    await subscribeLink.click();
                    await page.waitForTimeout(1000);
                    logger.info(`Clicked Subscribe link nth(${nthIndex}) for ${email}`);
                } catch (error) {
                    logger.warn(`Error clicking Subscribe link nth(${nthIndex}) for ${email}: ${error.message}`);
                    continue;
                }
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to Fox newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to Fox: ${error.message}`);
            throw error;
        }
    }
}

