import logging
from .base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class TheVergeScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.theverge.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            button = page.locator('xpath=/html/body/div[3]/div/a')
            await button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
            
            if await button.is_visible():
                await button.click()
            
            await page.locator("#newsletter-0").get_by_role("button", name="Select").click()
            await page.locator("#newsletter-").get_by_role("button", name="Select").click()
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to The Verge newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to The Verge: {e}")
            raise

