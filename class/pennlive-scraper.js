export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        console.log(`Starting subscription for ${email} to PennLive`);
        
        // Set up dialog handler
        page.once("dialog", async (dialog) => {
            await dialog.dismiss();
        });
        
        const newsletterClicks = [
            [".listing-button", "first", null],
            ["div:nth-child(2) > .newsletterlist__listings--listing-checkbox-label > .listing-button", null, null],
            ["div:nth-child(3) > .newsletterlist__listings--listing-checkbox-label > .listing-button", null, null],
            ["div:nth-child(4) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(5) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(6) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(7) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(8) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(9) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(10) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(11) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(12) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(13) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(16) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(17) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(18) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(19) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(20) > .newsletterlist__listings--listing-checkbox-label > .listing-button", null, null],
            ["div:nth-child(21) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
            ["div:nth-child(22) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", null, null],
        ];
        
        for (const [selector, modifier, pattern] of newsletterClicks) {
            try {
                let element;
                if (modifier === "first") {
                    element = page.locator(selector).first();
                } else {
                    element = page.locator(selector);
                }
                
                await element.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await element.scrollIntoViewIfNeeded();
                await page.waitForTimeout(500);
                await element.click();
                await page.waitForTimeout(1000);
            } catch (error) {
                console.warn(`Error clicking newsletter button '${selector}' for ${email}: ${error.message}`);
                continue;
            }
        }
        
        // Fill email address
        try {
            const emailInput = page.getByRole("textbox", { name: "Email" });
            await emailInput.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.waitForTimeout(1000);
            await emailInput.click();
            await emailInput.fill(email);
            await page.waitForTimeout(1000);
            console.log(`Filled email address field for ${email}`);
        } catch (error) {
            console.error(`Error filling email address for ${email}: ${error.message}`);
            throw error;
        }
        
        // Click Sign Up button
        try {
            const signupButton = page.locator('input#form-submit[type="submit"][value="Sign Up"]');
            await signupButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.waitForTimeout(1000);
            await signupButton.click();
            console.log(`Clicked Sign Up button for ${email}`);
            await page.waitForTimeout(3000);
            console.log(`Waiting for confirmation message for ${email}`);
        } catch (error) {
            console.error(`Error clicking Sign Up button for ${email}: ${error.message}`);
            throw error;
        }
        
        await page.waitForTimeout(5000);
        console.log(`Subscribed ${email} to PennLive newsletters`);
        return true;
    } catch (error) {
        console.error(`Error subscribing ${email} to PennLive: ${error.message}`);
        throw error;
    }
}

