export const BROWSER_TIMEOUT = 30000;

export async function subscribeEmail(page, email) {
    try {
        await page.pause();
        console.log(`Starting subscription for ${email} to Axios`);
        // TODO: Implement the subscription logic for Axios
        await page.waitForTimeout(5000);
        console.log(`Subscribed ${email} to Axios newsletters`);
    } catch (error) {
        console.error(`Error subscribing ${email} to Axios: ${error.message}`);
        throw error;
    }
}

