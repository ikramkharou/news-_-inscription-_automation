import logging
from .base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class AxiosScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.axios.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            
            #TODO: Implement the subscription logic for Axios
            button = page.locator('xpath=')
            await button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
            
            if await button.is_visible():
                await button.click()

            logger.info(f"Starting subscription for {email} to Axios")
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to Axios newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to Axios: {e}")
            raise

