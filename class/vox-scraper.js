export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        console.log(`Starting subscription for ${email} to Vox`);
        
        // Click labels in start-here section
        try {
            await page.locator("#start-here label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.locator("#start-here label").first().click();
            await page.waitForTimeout(3000);
            await page.locator("#start-here label").nth(1).click();
            await page.waitForTimeout(3000);
            await page.locator("#start-here label").nth(2).click();
            await page.waitForTimeout(3000);
            console.log(`Clicked start-here labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking start-here labels for ${email}: ${error.message}`);
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
            console.log(`Clicked politics-and-policy labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking politics-and-policy labels for ${email}: ${error.message}`);
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
            console.log(`Clicked future-perfect labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking future-perfect labels for ${email}: ${error.message}`);
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
            console.log(`Clicked culture-and-technology labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking culture-and-technology labels for ${email}: ${error.message}`);
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
            console.log(`Clicked build-new-habits labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking build-new-habits labels for ${email}: ${error.message}`);
        }
        
        // Click labels in just-for-fun section
        try {
            await page.locator("#just-for-fun label").first().waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.locator("#just-for-fun label").first().click();
            await page.waitForTimeout(3000);
            await page.locator("#just-for-fun label").nth(1).click();
            await page.waitForTimeout(3000);
            console.log(`Clicked just-for-fun labels for ${email}`);
        } catch (error) {
            console.warn(`Error clicking just-for-fun labels for ${email}: ${error.message}`);
        }
        
        // Fill email address
        try {
            const emailInput = page.locator("#email");
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
            const signupButton = page.locator('xpath=//*[@id="content"]/div[1]/div/div/form/div/div[2]/fieldset/div/button');
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
        console.log(`Subscribed ${email} to Vox newsletters`);
    } catch (error) {
        console.error(`Error subscribing ${email} to Vox: ${error.message}`);
        throw error;
    }
}

