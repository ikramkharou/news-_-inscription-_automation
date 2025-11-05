import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class TheVergeScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.theverge.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to The Verge")
            
            # Click labels in free-newsletters section
            try:
                await page.locator("#free-newsletters label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#free-newsletters label").first.click()
                await page.wait_for_timeout(3000)  
                await page.locator("#free-newsletters label").nth(1).click()
                await page.wait_for_timeout(3000)  
                logger.info(f"Clicked free-newsletters labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking free-newsletters labels for {email}: {e}")
            
            # Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Enter your email")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await email_input.click()
                await page.wait_for_timeout(3000)  
                await email_input.fill(email)
                await page.wait_for_timeout(3000)  
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Click Sign Up button
            try:
                signup_button = page.get_by_role("button", name="Sign Up")
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await signup_button.click()
                logger.info(f"Clicked Sign Up button for {email}")
                await page.wait_for_timeout(3000)
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Sign Up button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to The Verge newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to The Verge: {e}")
            raise

