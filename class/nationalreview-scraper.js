export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    const maxAttempts = 2;
    
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        try {
            console.log(`Starting subscription attempt ${attempt + 1} for ${email} to National Review`);
            
            // Step 1: Click checkbox 4
            try {
                const checkbox = page.locator("div:nth-child(4) > .checkbox > .checkmark");
                await checkbox.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await checkbox.scrollIntoViewIfNeeded();
                await page.waitForTimeout(500);
                await checkbox.click();
                await page.waitForTimeout(1000);
                console.log(`Clicked checkbox 4 for ${email}`);
            } catch (error) {
                console.warn(`Error clicking checkbox 4 for ${email}: ${error.message}`);
            }
            
            // Step 2: Fill email and click SIGN UP
            try {
                const emailInput = page.getByRole("textbox", { name: "Email Address" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await emailInput.click();
                await emailInput.fill(email);
                await page.waitForTimeout(1000);
                console.log(`Filled email address for ${email}`);
                
                const signupButton = page.getByRole("button", { name: "SIGN UP" });
                await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await signupButton.click();
                await page.waitForTimeout(2000);
                console.log(`Clicked SIGN UP button for ${email}`);
            } catch (error) {
                console.warn(`Error in first email/SIGN UP step for ${email}: ${error.message}`);
            }
            
            // Step 3: Click all checkboxes
            try {
                const checkboxesToClick = [
                    ".checkmark", // first
                    "div:nth-child(2) > .checkbox > .checkmark",
                    "div:nth-child(3) > .checkbox > .checkmark",
                    "div:nth-child(4) > .checkbox > .checkmark",
                    "div:nth-child(5) > .checkbox > .checkmark",
                    "div:nth-child(6) > .checkbox > .checkmark",
                    "div:nth-child(7) > .checkbox > .checkmark",
                    "div:nth-child(8) > .checkbox > .checkmark",
                    "div:nth-child(9) > .checkbox > .checkmark",
                ];
                
                for (const checkboxSelector of checkboxesToClick) {
                    try {
                        const checkbox = checkboxSelector === ".checkmark"
                            ? page.locator(checkboxSelector).first()
                            : page.locator(checkboxSelector);
                        
                        await checkbox.waitFor({ state: 'visible', timeout: 5000 });
                        await checkbox.scrollIntoViewIfNeeded();
                        await page.waitForTimeout(300);
                        await checkbox.click();
                        await page.waitForTimeout(500);
                        console.log(`Clicked checkbox ${checkboxSelector} for ${email}`);
                    } catch (error) {
                        console.warn(`Error clicking checkbox ${checkboxSelector} for ${email}: ${error.message}`);
                        continue;
                    }
                }
            } catch (error) {
                console.warn(`Error clicking checkboxes for ${email}: ${error.message}`);
            }
            
            // Step 4: Fill email again
            try {
                const emailInput = page.getByRole("textbox", { name: "Email Address" });
                await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await page.waitForTimeout(1000);
                await emailInput.click();
                await emailInput.fill(email);
                await page.waitForTimeout(1000);
                console.log(`Filled email address again for ${email}`);
            } catch (error) {
                console.warn(`Error filling email again for ${email}: ${error.message}`);
            }
            
            await page.waitForTimeout(3000);
            
            if (attempt === maxAttempts - 1) {
                console.log(`Completed all ${maxAttempts} attempts for ${email}`);
                break;
            }
            
            await page.waitForTimeout(2000);
        } catch (error) {
            console.error(`Error in attempt ${attempt + 1} for ${email}: ${error.message}`);
            if (attempt === maxAttempts - 1) {
                console.error(`All attempts failed for ${email}, closing browser`);
                throw error;
            }
        }
    }
    
    await page.waitForTimeout(5000);
    console.log(`Subscribed ${email} to National Review newsletters`);
}

