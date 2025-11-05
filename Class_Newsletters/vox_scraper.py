import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class VoxScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.vox.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to Vox")
            
            # Click labels in start-here section
            try:
                await page.locator("#start-here label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#start-here label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#start-here label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#start-here label").nth(2).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked start-here labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking start-here labels for {email}: {e}")
            
            # Click labels in politics-and-policy section
            try:
                await page.locator("#politics-and-policy label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#politics-and-policy label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#politics-and-policy label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#politics-and-policy label").nth(2).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#politics-and-policy label").nth(3).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked politics-and-policy labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking politics-and-policy labels for {email}: {e}")
            
            # Click labels in future-perfect section
            try:
                await page.locator("#future-perfect label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#future-perfect label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#future-perfect label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#future-perfect label").nth(2).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked future-perfect labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking future-perfect labels for {email}: {e}")
            
            # Click labels in culture-and-technology section
            try:
                await page.locator("#culture-and-technology label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#culture-and-technology label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#culture-and-technology label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#culture-and-technology label").nth(2).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#culture-and-technology label").nth(3).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked culture-and-technology labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking culture-and-technology labels for {email}: {e}")
            
            # Click labels in build-new-habits section
            try:
                await page.locator("#build-new-habits label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#build-new-habits label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#build-new-habits label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#build-new-habits label").nth(2).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked build-new-habits labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking build-new-habits labels for {email}: {e}")
            
            # Click labels in just-for-fun section
            try:
                await page.locator("#just-for-fun label").first.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.locator("#just-for-fun label").first.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                await page.locator("#just-for-fun label").nth(1).click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                logger.info(f"Clicked just-for-fun labels for {email}")
            except Exception as e:
                logger.warning(f"Error clicking just-for-fun labels for {email}: {e}")
            
            # Fill email address
            try:
                email_input = page.locator("#email")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await email_input.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds before filling
                await email_input.fill(email)
                await page.wait_for_timeout(3000)  # Wait 3 seconds after filling
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Click Sign Up button
            try:
                signup_button = page.locator('xpath=//*[@id="content"]/div[1]/div/div/form/div/div[2]/fieldset/div/button')
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await signup_button.click()
                logger.info(f"Clicked Sign Up button for {email}")
                await page.wait_for_timeout(3000)
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Sign Up button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to Vox newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to Vox: {e}")
            raise

