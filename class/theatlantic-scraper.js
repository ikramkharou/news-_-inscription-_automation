import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class TheAtlanticScraper extends BaseScraper {
    getUrl() {
        return "https://www.theatlantic.com/newsletters/";
    }

    async subscribeEmail(page, email) {
        try {
            logger.info(`Starting subscription for ${email} to The Atlantic`);
            
            const newsletterClicks = [
                "Weekday MorningsThe Atlantic",
                "Weekday Evenings and Sunday",
                "At least once a weekTrump's",
                "Weekday and Sunday",
                "Sunday EveningsThis WeekAn",
                "As editor's notes are",
                "Thursday MorningsHow to Build",
                "WeeklyThe Weekly PlanetThe",
                "WeeklyWork in ProgressDerek",
                "WeeklyBeing HumanOur health",
                "As new articles are publishedGalaxy BrainA newsletter from Charlie Warzel about",
                "As new articles are publishedDeep ShtetlYair Rosenberg demystifies the often",
                "Every TuesdayDear JamesIn his",
                "WeeklyAtlantic",
                "As new photo essays are",
                "WeeklyTime-Travel",
            ];
            
            for (const text of newsletterClicks) {
                try {
                    let listitem = page.getByRole("listitem").filter({ hasText: text });
                    try {
                        await listitem.waitFor({ state: 'visible', timeout: 5000 });
                    } catch (timeoutError) {
                        logger.warn(`Exact match timed out for '${text}', trying partial match for ${email}`);
                        listitem = page.getByRole("listitem").filter({ hasText: text.length > 30 ? text.substring(0, 30) : text });
                        await listitem.waitFor({ state: 'visible', timeout: 5000 });
                    }
                    
                    await listitem.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(1000);
                    
                    const element = listitem.getByRole("paragraph").nth(1);
                    await element.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                    
                    try {
                        await element.click({ timeout: 5000 });
                        await page.waitForTimeout(1000);
                    } catch (clickError) {
                        if (clickError.message.includes("intercepts") || clickError.message.toLowerCase().includes("intercepted")) {
                            logger.warn(`Click intercepted for '${text}', trying force click for ${email}`);
                            await element.click({ force: true });
                            await page.waitForTimeout(1000);
                        } else {
                            throw clickError;
                        }
                    }
                    
                    await page.waitForTimeout(1000);
                } catch (error) {
                    logger.warn(`Error clicking newsletter item '${text}' for ${email}: ${error.message}`);
                    continue;
                }
            }
            
            // Click "Select" buttons
            try {
                for (let i = 0; i < 4; i++) {
                    const selectButton = page.getByText("Select", { exact: true }).first();
                    await selectButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                    await page.waitForTimeout(1000);
                    await selectButton.click();
                    await page.waitForTimeout(3000);
                    logger.info(`Clicked Select button ${i+1} (first) for ${email}`);
                }
                
                const selectButton = page.getByText("Select", { exact: true });
                await selectButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await selectButton.click();
                await page.waitForTimeout(3000);
                logger.info(`Clicked Select button 5 (no first) for ${email}`);
            } catch (error) {
                logger.warn(`Error clicking Select buttons for ${email}: ${error.message}`);
            }
            
            // Fill email address
            try {
                const emailInput = page.getByRole("textbox", { name: "Email Address" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(3000);
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
                await page.waitForTimeout(3000);
                await signupButton.click();
                logger.info(`Clicked Sign Up button for ${email}`);
                await page.waitForTimeout(3000);
                logger.info(`Waiting for confirmation message for ${email}`);
            } catch (error) {
                logger.error(`Error clicking Sign Up button for ${email}: ${error.message}`);
                throw error;
            }
            
            await page.waitForTimeout(5000);
            logger.info(`Subscribed ${email} to The Atlantic newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to The Atlantic: ${error.message}`);
            throw error;
        }
    }
}

