export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        console.log(`Starting subscription for ${email} to TechCrunch`);
        
        // Click "Select All" button
        try {
            const selectAllButton = page.getByRole("button", { name: "Select All", exact: true });
            await selectAllButton.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await page.waitForTimeout(1000);
            await selectAllButton.click();
            await page.waitForTimeout(1000);
            console.log(`Clicked Select All button for ${email}`);
        } catch (error) {
            console.error(`Error clicking Select All button for ${email}: ${error.message}`);
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
            console.log(`Filled email address field for ${email}`);
        } catch (error) {
            console.error(`Error filling email address for ${email}: ${error.message}`);
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
                    console.log(`Clicked Subscribe button ${clickNumber + 1} (human-like click) for ${email}`);
                } catch (clickError) {
                    if (clickError.message.toLowerCase().includes("intercepts") || clickError.message.toLowerCase().includes("intercepted")) {
                        console.warn(`Click intercepted, trying force click for ${email}`);
                        await subscribeButton.click({ force: true, delay: 100 });
                        console.log(`Clicked Subscribe button ${clickNumber + 1} (force click) for ${email}`);
                    } else {
                        console.warn(`Regular click failed, trying JavaScript click for ${email}`);
                        await subscribeButton.evaluate(element => element.click());
                        console.log(`Clicked Subscribe button ${clickNumber + 1} (JavaScript click) for ${email}`);
                    }
                }
                
                if (clickNumber < 1) {
                    await page.waitForTimeout(500);
                }
            }
            
            await page.waitForTimeout(3000);
            console.log(`Waiting for confirmation message for ${email}`);
        } catch (error) {
            console.error(`Error clicking Subscribe button for ${email}: ${error.message}`);
            throw error;
        }
        
        await page.waitForTimeout(5000);
        console.log(`Subscribed ${email} to TechCrunch newsletters`);
    } catch (error) {
        console.error(`Error subscribing ${email} to TechCrunch: ${error.message}`);
        throw error;
    }
}

