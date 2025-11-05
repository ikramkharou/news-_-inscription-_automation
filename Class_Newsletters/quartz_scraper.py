import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class QuartzScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://qz.com/newsletter"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            await page.pause()
            logger.info(f"Starting subscription for {email} to Quartz")
            
            # Click and fill email address
            try:
                email_input = page.get_by_role("textbox", name="Enter email here")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking email field
                await email_input.click()
                await email_input.fill(email)
                await page.wait_for_timeout(1000)  # Wait after filling email
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Wait for "Sign me up" button to be visible and click it
            try:
                # Wait for the button to appear after filling email
                signup_button = page.get_by_role("button", name="Sign me up")
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking button
                
                # Scroll button into view if needed
                await signup_button.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)  # Wait for scroll
                
                # Click the Sign me up button
                await signup_button.click()
                logger.info(f"Clicked Sign me up button for {email}")
                await page.wait_for_timeout(3000)  # Wait for confirmation
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Sign me up button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to Quartz newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to Quartz: {e}")
            raise

