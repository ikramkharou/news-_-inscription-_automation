export const BROWSER_TIMEOUT = 30000;
const MAX_NEWSLETTERS = 20;

// Helper: Random wait
function waitRandom(minSec, maxSec) {
    return new Promise(resolve => {
        const waitTime = Math.random() * (maxSec - minSec) + minSec;
        setTimeout(resolve, waitTime * 1000);
    });
}

// Helper: Find email input field using simple JavaScript query
async function findEmailField(page) {
    try {
        // First try input[type="email"]
        const emailInput = page.locator('input[type="email"]').first();
        if (await emailInput.isVisible().catch(() => false)) {
            console.log("Found email field");
            return emailInput;
        }
        
        // Then try finding by name, placeholder, or id
        const allInputs = await page.locator('input').all();
        for (const input of allInputs) {
            try {
                const name = await input.getAttribute('name').catch(() => '');
                const placeholder = await input.getAttribute('placeholder').catch(() => '');
                const id = await input.getAttribute('id').catch(() => '');
                
                if (name?.toLowerCase().includes('email') || 
                    placeholder?.toLowerCase().includes('email') ||
                    id?.toLowerCase().includes('email')) {
                    if (await input.isVisible().catch(() => false)) {
                        console.log("Found email field");
                        return input;
                    }
                }
            } catch (e) {
                continue;
            }
        }
        
        return null;
    } catch (e) {
        console.warn(`Error finding email field: ${e.message}`);
        return null;
    }
}

// Helper: Find submit/subscribe button using multiple strategies
async function findSubmitButton(page) {
    // Try Fox News specific structure first
    try {
        const foxNewsButton = page.locator('div.button.enter a').first();
        if (await foxNewsButton.isVisible().catch(() => false)) {
            console.log("Found Fox News specific submit button");
            return foxNewsButton;
        }
    } catch (e) {
        // Continue to next method
    }
    
    // Try JavaScript search
    try {
        const submitButton = await page.evaluate(() => {
            // First try Fox News specific structure
            const foxNewsButton = document.querySelector('div.button.enter a');
            if (foxNewsButton && foxNewsButton.textContent.toLowerCase().includes('subscribe')) {
                return true;
            }
            
            // Then try general search
            const elements = document.querySelectorAll('button, a, input[type="submit"], input[type="button"]');
            for (const element of elements) {
                const text = (element.textContent || element.innerText || '').toLowerCase().trim();
                const title = (element.getAttribute('title') || '').toLowerCase().trim();
                const className = (element.getAttribute('class') || '').toLowerCase();
                const id = (element.getAttribute('id') || '').toLowerCase();
                
                if (text.includes('subscribe') || 
                    text.includes('submit') ||
                    text.includes('sign up') ||
                    text.includes('continue') ||
                    text.includes('send') ||
                    title.includes('subscribe') ||
                    className.includes('submit') ||
                    className.includes('subscribe') ||
                    id.includes('submit') ||
                    id.includes('subscribe')) {
                    if (element.offsetParent !== null) { // Check if visible
                        return true;
                    }
                }
            }
            return false;
        });
        
        if (submitButton) {
            console.log("Found submit button using JavaScript search");
            return page.locator('div.button.enter a').first().or(
                page.locator('button, a').filter({ hasText: /subscribe|submit/i }).first()
            );
        }
    } catch (e) {
        // Continue
    }
    
    return null;
}

// Helper: Find all subscribe buttons on the page
async function findSubscribeButtons(page) {
    try {
        console.log("Searching for subscribe buttons...");
        
        // Get all potential button elements
        const allElements = await page.locator('button, a, input[type="button"], input[type="submit"]').all();
        const buttons = [];
        
        for (const element of allElements) {
            try {
                const text = (await element.textContent().catch(() => '') || '').toLowerCase().trim();
                const title = (await element.getAttribute('title').catch(() => '') || '').toLowerCase().trim();
                const className = (await element.getAttribute('class').catch(() => '') || '').toLowerCase();
                const id = (await element.getAttribute('id').catch(() => '') || '').toLowerCase();
                
                // Look for subscribe buttons specifically
                if (text === 'subscribe' || 
                    text.includes('subscribe') ||
                    title.includes('subscribe') ||
                    className.includes('subscribe') ||
                    id.includes('subscribe')) {
                    buttons.push(element);
                }
            } catch (e) {
                // Skip this element
                continue;
            }
        }
        
        console.log(`Found ${buttons.length} subscribe buttons`);
        return buttons;
    } catch (e) {
        console.log(`Error finding subscribe buttons: ${e.message}`);
        return [];
    }
}

// Main function: Subscribe to newsletters
export async function subscribeEmail(page, email) {
    try {
        console.log("FOX NEWS SUBSCRIPTION: Starting...");
        
        // Find all subscribe buttons
        const subscribeButtons = await findSubscribeButtons(page);
        
        if (subscribeButtons.length < 5) {
            console.log(`Only found ${subscribeButtons.length} subscribe buttons, expected more`);
            return false;
        }
        
        console.log(`Found ${subscribeButtons.length} subscribe buttons, targeting ${MAX_NEWSLETTERS} subscriptions`);
        
        // Process each newsletter: click subscribe → fill email → click subscribe again (confirmation)
        let clickedCount = 0;
        let failedClicks = 0;
        const targetClicks = Math.min(MAX_NEWSLETTERS, subscribeButtons.length);
        
        for (let i = 0; i < subscribeButtons.length; i++) {
            if (clickedCount >= targetClicks) {
                console.log(`Reached target of ${targetClicks} subscriptions`);
                break;
            }
            
            try {
                const button = subscribeButtons[i];
                const isVisible = await button.isVisible().catch(() => false);
                
                if (isVisible) {
                    const buttonText = await button.textContent().catch(() => `button-${i+1}`);
                    console.log(`Processing newsletter ${i+1}: '${buttonText.substring(0, 50)}'`);
                    
                    // Scroll to button (fast)
                    await button.evaluate((el) => {
                        el.scrollIntoView({ block: 'center', behavior: 'instant' });
                    });
                    await page.waitForTimeout(200);  // Minimal wait
                    
                    // FIRST CLICK: Click subscribe button ONCE (fast)
                    console.log(`Clicking subscribe button ${i+1}...`);
                    let clickSuccess = false;
                    
                    // Try fast JavaScript click first
                    try {
                        await button.evaluate(el => el.click());
                        clickSuccess = true;
                    } catch (e) {
                        // Fallback to regular click
                        try {
                            await button.click({ timeout: 2000, force: true });
                            clickSuccess = true;
                        } catch (e2) {
                            // Click failed
                        }
                    }
                    
                    if (!clickSuccess) {
                        failedClicks++;
                        console.log(`Failed to click subscribe button ${i+1}`);
                        continue;
                    }
                    
                    console.log(`Clicked subscribe button ${i+1}`);
                    await waitRandom(0.5, 1);  // Reduced wait time
                    
                    // Wait for email field (faster)
                    let emailField = null;
                    const maxWaitTime = 5;  // Reduced from 10
                    let waitTime = 0;
                    
                    while (waitTime < maxWaitTime && !emailField) {
                        emailField = await findEmailField(page);
                        if (emailField) {
                            break;
                        }
                        await page.waitForTimeout(500);  // Faster check
                        waitTime += 0.5;
                        if (waitTime % 1 === 0) {
                            console.log(`Waiting for email field... (${waitTime}s)`);
                        }
                    }
                    
                    if (!emailField) {
                        console.log(`Email field did not appear for newsletter ${i+1}`);
                        failedClicks++;
                        continue;
                    }
                    
                    // Check if email is already filled
                    try {
                        const existingEmail = await emailField.inputValue().catch(() => '');
                        if (existingEmail.trim() && existingEmail.trim() === email.trim()) {
                            console.log(`Email already filled for newsletter ${i+1}: '${existingEmail.substring(0, 30)}'`);
                        } else {
                            // Fill email field
                            console.log(`Filling email field for newsletter ${i+1}...`);
                            await emailField.clear();
                            await emailField.fill(email);
                            console.log(`Filled email: ${email}`);
                        }
                    } catch (e) {
                        console.log(`Failed to fill email field: ${e.message}`);
                        failedClicks++;
                        continue;
                    }
                    
                    // Find and click submit button (div.button.enter a)
                    console.log(`Looking for submit button (div.button.enter a) for newsletter ${i+1}...`);
                    let submitButton = null;
                    
                    // Try Fox News specific structure first
                    try {
                        const foxButton = page.locator('div.button.enter a').first();
                        if (await foxButton.isVisible().catch(() => false)) {
                            submitButton = foxButton;
                            console.log(`Found submit button using: div.button.enter a`);
                        }
                    } catch (e) {
                        // Continue
                    }
                    
                    // If not found, try JavaScript search
                    if (!submitButton) {
                        try {
                            const found = await page.evaluate(() => {
                                const foxNewsButton = document.querySelector('div.button.enter a');
                                if (foxNewsButton && foxNewsButton.textContent.toLowerCase().includes('subscribe')) {
                                    return true;
                                }
                                return false;
                            });
                            
                            if (found) {
                                submitButton = page.locator('div.button.enter a').first();
                                console.log(`Found submit button using JavaScript search`);
                            }
                        } catch (e) {
                            // Continue
                        }
                    }
                    
                    // Fallback to findSubmitButton
                    if (!submitButton) {
                        submitButton = await findSubmitButton(page);
                    }
                    
                    if (!submitButton) {
                        console.log(`No submit button found for newsletter ${i+1}`);
                        failedClicks++;
                        continue;
                    }
                    
                    // Click submit button (optimized for speed - no scroll wait)
                    console.log(`Clicking submit button for newsletter ${i+1}...`);
                    let submitClickSuccess = false;
                    
                    try {
                        // Fast JavaScript click (no scroll wait, instant)
                        try {
                            await submitButton.evaluate((el) => {
                                el.scrollIntoView({ block: 'center', behavior: 'instant' });
                                el.click();
                            });
                            submitClickSuccess = true;
                            console.log(`Clicked submit button (fast method)`);
                        } catch (e) {
                            // Fallback to regular click with short timeout
                            try {
                                await submitButton.click({ timeout: 2000, force: true });
                                submitClickSuccess = true;
                                console.log(`Clicked submit button (force method)`);
                            } catch (e2) {
                                console.log(`Error clicking submit button: ${e2.message}`);
                            }
                        }
                    } catch (e) {
                        console.log(`Error clicking submit button: ${e.message}`);
                    }
                    
                    if (submitClickSuccess) {
                        clickedCount++;
                        console.log(`Successfully completed subscription ${clickedCount}!`);
                        await waitRandom(0.5, 1);  // Reduced wait time
                    } else {
                        failedClicks++;
                        console.log(`Failed to click submit button for newsletter ${i+1}`);
                    }
                }
            } catch (e) {
                failedClicks++;
                console.log(`Error with newsletter ${i+1}: ${e.message.substring(0, 100)}`);
                continue;
            }
        }
        
        console.log(`SUBSCRIPTION COMPLETE: ${clickedCount} successful, ${failedClicks} failed`);
        
        if (clickedCount === 0) {
            throw new Error(`Failed to subscribe: ${failedClicks} failed attempts`);
        }
        
        console.log(`Successfully subscribed to ${clickedCount} newsletter(s)`);
    } catch (error) {
        console.error(`Error in subscription process: ${error.message}`);
        throw error;
    }
}
