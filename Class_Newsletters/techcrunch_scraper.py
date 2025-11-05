import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class TechCrunchScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://techcrunch.com/newsletters/"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to TechCrunch")
            
            # Click "Select All" button
            try:
                select_all_button = page.get_by_role("button", name="Select All", exact=True)
                await select_all_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking
                await select_all_button.click()
                await page.wait_for_timeout(1000)  # Wait after clicking
                logger.info(f"Clicked Select All button for {email}")
            except Exception as e:
                logger.error(f"Error clicking Select All button for {email}: {e}")
                raise
            
            # Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Email address")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking email field
                await email_input.click()
                await page.wait_for_timeout(1000)  # Wait after clicking, before filling
                await email_input.fill(email)
                await page.wait_for_timeout(1000)  # Wait after filling email
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Click Subscribe button using XPath (like human)
            try:
                # Use the specific XPath provided for more reliable clicking
                subscribe_button = page.locator('xpath=/html/body/div[3]/main/div/form/div/div[3]/div/div/div[2]/fieldset/div[2]/div/div/div/button')
                await subscribe_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                
                # Scroll the button into view smoothly (human-like)
                await subscribe_button.scroll_into_view_if_needed()
                await page.wait_for_timeout(1000)  # Wait for scroll to complete


                for click_number in range(2):
                    # Use normal click with human-like delay
                    try:
                        # Move mouse to button first (more human-like)
                        box = await subscribe_button.bounding_box()
                        if box:
                            await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                            await page.wait_for_timeout(200)  # Small delay before clicking
                        
                        await subscribe_button.click(timeout=5000, delay=100)  # Add delay to simulate human click
                        logger.info(f"Clicked Subscribe button {click_number + 1} (human-like click) for {email}")
                    except Exception as click_error:
                        # If normal click fails, try force click
                        if "intercepts" in str(click_error).lower() or "intercepted" in str(click_error).lower():
                            logger.warning(f"Click intercepted, trying force click for {email}")
                            await subscribe_button.click(force=True, delay=100)
                            logger.info(f"Clicked Subscribe button {click_number + 1} (force click) for {email}")
                        else:
                            # Last resort: try JavaScript click
                            logger.warning(f"Regular click failed, trying JavaScript click for {email}")
                            await subscribe_button.evaluate("element => element.click()")
                            logger.info(f"Clicked Subscribe button {click_number + 1} (JavaScript click) for {email}")
                    

                    # Wait a bit between clicks (simulating human behavior)
                    if click_number < 1:  # Don't wait after the last click
                        await page.wait_for_timeout(500)  # Small delay between clicks
                
                await page.wait_for_timeout(3000)  # Wait for confirmation
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Subscribe button for {email}: {e}")
                raise


            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to TechCrunch newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to TechCrunch: {e}")
            raise

