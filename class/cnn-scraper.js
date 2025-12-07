import { BaseScraper } from '../core/base-scraper.js';
import { logger, BROWSER_TIMEOUT } from '../config.js';

export class CNNScraper extends BaseScraper {
    getUrl() {
        return "https://edition.cnn.com/newsletters";
    }

    async subscribeEmail(page, email) {
        try {
            // Implement the subscription logic for CNN
            await page.pause();
            
            const button = page.locator('xpath=/html/body/div[3]/div/a');
            try {
                await button.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                if (await button.isVisible()) {
                    await button.click();
                    logger.info(`Clicked navigation start button for ${email}`);
                }
            } catch (error) {
                logger.info(`Navigation button not visible for ${email}, proceeding to select buttons directly`);
            }

            let clickedCount = 0;
            for (let i = 0; i < 2; i++) {
                try {
                    const newsletterLocator = page.locator(`#newsletter-${i}`).getByRole("button", { name: "Select" });
                    await newsletterLocator.click();
                    clickedCount++;
                    logger.info(`Clicked newsletter-${i} button for ${email}`);
                } catch (error) {
                    logger.debug(`Newsletter-${i} button not found or not clickable`);
                    continue;
                }
            }

            try {
                const newsletterEmpty = page.locator("#newsletter-").getByRole("button", { name: "Select" });
                await newsletterEmpty.click();
                clickedCount++;
                logger.info(`Clicked newsletter- button for ${email}`);
            } catch (error) {
                logger.debug(`Newsletter- button not found or not clickable`);
            }

            logger.info(`Successfully clicked ${clickedCount} newsletter buttons for ${email}`);

            // Fill email address and click sign up button
            try {
                const emailInput = page.getByRole("textbox", { name: "Email address" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await emailInput.fill(email);
                logger.info(`Filled email address field for ${email}`);
                
                const signupButton = page.getByRole("button", { name: "Sign Up", exact: true });
                await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await signupButton.click();
                logger.info(`Clicked Sign Up button for ${email}`);
            } catch (error) {
                logger.error(`Error filling email or clicking Sign Up for ${email}: ${error.message}`);
                throw error;
            }

            // Click start puzzle button for Arkose Labs captcha
            try {
                await page.waitForTimeout(3000);
                
                let startPuzzleClicked = false;
                
                try {
                    const verificationFrame = page.frameLocator("iframe[title=\"Verification challenge\"]");
                    const visualFrame = verificationFrame.frameLocator("iframe[title=\"Visual challenge\"]");
                    
                    const startPuzzleButton = visualFrame.locator('xpath=/html/body/div/div/div[1]/button');
                    try {
                        await startPuzzleButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                        if (await startPuzzleButton.isVisible()) {
                            await startPuzzleButton.click();
                            logger.info(`Clicked Start Puzzle button (xpath method) for ${email}`);
                            startPuzzleClicked = true;
                        }
                    } catch (error) {
                        logger.debug(`Start Puzzle button not visible (xpath method) for ${email}`);
                    }
                } catch (error) {
                    logger.debug(`Failed to find Start Puzzle button with xpath method: ${error.message}`);
                }
                
                if (!startPuzzleClicked) {
                    try {
                        const dialog = page.getByRole("dialog");
                        const verificationFrame = await dialog.locator("iframe[title=\"Verification challenge\"]").contentFrame();
                        const visualFrame = await verificationFrame.locator("iframe[title=\"Visual challenge\"]").contentFrame();
                        
                        const startPuzzleButton = visualFrame.getByRole("button", { name: "Start Puzzle" });
                        await startPuzzleButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                        await startPuzzleButton.click();
                        logger.info(`Clicked Start Puzzle button (get_by_role method) for ${email}`);
                    } catch (error) {
                        logger.warn(`Failed to click Start Puzzle button with get_by_role method: ${error.message}`);
                    }
                }
            } catch (error) {
                logger.warn(`Captcha handling failed for ${email}: ${error.message}`);
            }
            
            await page.waitForTimeout(50000);
            logger.info(`Subscribed ${email} to CNN newsletters`);
        } catch (error) {
            logger.error(`Error subscribing ${email} to CNN: ${error.message}`);
            throw error;
        }
    }
}

