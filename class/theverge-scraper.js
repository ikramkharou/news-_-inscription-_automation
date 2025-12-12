export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        console.log(`Starting subscription for ${email} to The Verge`);
        
        // Click labels in free-newsletters section
        try {
            await page.locator("#free-newsletters label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.locator("#free-newsletters label").first().click();
            await page.waitForTimeout(3000);
            await page.locator("#free-newsletters label").nth(1).click();
            await page.waitForTimeout(3000);
            console.log(`Clicked free-newsletters labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking free-newsletters labels for ${email}: ${error.message}`);
        }
        
        // Fill email address
        try {
            const emailInput = page.getByRole("textbox", { name: "Enter your email" });
            await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await emailInput.click();
            await page.waitForTimeout(3000);
            await emailInput.fill(email);
            await page.waitForTimeout(3000);
            console.log(`Filled email address field for ${email}`);
        } catch (error) {
            console.error(`Error filling email address for ${email}: ${error.message}`);
            throw error;
        }
        
        // Click Sign Up button
        try {
            const signupButton = page.getByRole("button", { name: "Sign Up" });
            await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await signupButton.click();
            console.log(`Clicked Sign Up button for ${email}`);
            await page.waitForTimeout(3000);
            console.log(`Waiting for confirmation message for ${email}`);
        } catch (error) {
            console.error(`Error clicking Sign Up button for ${email}: ${error.message}`);
            throw error;
        }
        
        await page.waitForTimeout(5000);
        console.log(`Subscribed ${email} to The Verge newsletters`);
    } catch (error) {
        console.error(`Error subscribing ${email} to The Verge: ${error.message}`);
        throw error;
    }
}

