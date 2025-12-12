export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        console.log(`Starting subscription for ${email} to The Guardian`);
        
        const newsletterButtons = [
            "add Detox Your Kitchen to",
            "add This Week in Trumpland to",
            "add The Long Wave to",
            "add First Thing to subscribe",
            "add The Overwhelm to",
            "add Fighting Back to",
            "add Well Actually to",
            "add Reclaim your brain to",
            "add Trump on Trial to",
            "add Soccer with Jonathan",
            "add Down to Earth to",
            "add Follow Mehdi Hasan to",
            "add Follow Robert Reich to",
            "add Follow Margaret Sullivan",
            "add The Week in Patriarchy to",
            "add This is Europe to",
            "add TechScape to subscribe",
            "add Fashion Statement to",
            "add The Guide to subscribe",
            "add Film Weekly to subscribe",
            "add Sleeve Notes to subscribe",
            "add What's On to subscribe",
            "add Art Weekly to subscribe",
            "add Documentaries to",
            "add Inside Saturday to",
            "add Five Great Reads to",
            "add The Upside to subscribe",
            "add The Long Read to",
            "add Saved for Later to",
            "add House to Home to",
            "add Global Dispatch to",
            "add Cotton Capital to",
            "add The Traveller to",
            "add Her Stage to subscribe",
            "add The Crunch to subscribe",
            "add Football Daily to",
            "add Moving the Goalposts to",
            "add The Spin to subscribe list",
            "add The Breakdown to",
            "add The Recap to subscribe",
            "add Australia Sport to",
            "add Headlines US to subscribe",
            "add Opinion US to subscribe",
            "add Headlines UK to subscribe",
            "add Opinion UK to subscribe",
            "add Opinion AUS to subscribe",
            "add Headlines Europe to",
            "add Business Today to",
            "add Headlines AUS to",
            "add First Edition to",
            "add Saturday Edition to",
            "add Morning Mail to subscribe",
            "add Afternoon Update to",
            "add Australian Politics to"
        ];
        
        for (const buttonName of newsletterButtons) {
            try {
                const button = page.getByRole("button", { name: buttonName });
                await button.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await button.click();
                await page.waitForTimeout(3000);
            } catch (error) {
                console.warn(`Error clicking newsletter button '${buttonName}' for ${email}: ${error.message}`);
                continue;
            }
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
        
        // Check the updates checkbox
        try {
            const updatesCheckbox = page.getByRole("checkbox", { name: "Get updates about our" });
            await updatesCheckbox.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await updatesCheckbox.check();
            await page.waitForTimeout(3000);
            console.log(`Toggled updates checkbox for ${email}`);
        } catch (error) {
            console.warn(`Error toggling updates checkbox for ${email}: ${error.message}`);
        }
        
        // Click reCAPTCHA checkbox in iframe
        try {
            const iframe = page.locator("iframe[name=\"a-xhsigsb8cosx\"]");
            await iframe.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            const frame = await iframe.contentFrame();
            if (frame) {
                const recaptchaCheckbox = frame.getByRole("checkbox", { name: "I'm not a robot" });
                await recaptchaCheckbox.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
                await recaptchaCheckbox.click();
                await page.waitForTimeout(3000);
                console.log(`Clicked reCAPTCHA checkbox for ${email}`);
            }
        } catch (error) {
            console.warn(`Error clicking reCAPTCHA checkbox for ${email}: ${error.message}`);
        }
        
        // Click the final div element
        try {
            const finalDiv = page.locator("div:nth-child(13) > div").first();
            await finalDiv.waitFor({ state: 'visible', timeout: BROWSER_TIMEOUT });
            await finalDiv.click();
            await page.waitForTimeout(3000);
            console.log(`Clicked final div element for ${email}`);
        } catch (error) {
            console.warn(`Error clicking final div element for ${email}: ${error.message}`);
        }
        
        await page.waitForTimeout(5000);
        console.log(`Subscribed ${email} to The Guardian newsletters`);
    } catch (error) {
        console.error(`Error subscribing ${email} to The Guardian: ${error.message}`);
        throw error;
    }
}



