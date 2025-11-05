import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class FoxScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.foxnews.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to Fox")
            
            # Step 1: Click first subscribe button
            try:
                subscribe_button = page.locator(".button.subscribe > a").first
                await subscribe_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking
                await subscribe_button.click()
                await page.wait_for_timeout(1000)  # Wait after clicking
                logger.info(f"Clicked first subscribe button for {email}")
            except Exception as e:
                logger.error(f"Error clicking first subscribe button for {email}: {e}")
                raise
            
            # Step 2: Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Type your email")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking email field
                await email_input.click()
                await email_input.fill(email)
                await page.wait_for_timeout(1000)  # Wait after filling email
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Step 3: Click enter button
            try:
                enter_button = page.locator(".button.enter > a").first
                await enter_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking
                await enter_button.click()
                await page.wait_for_timeout(2000)  # Wait after clicking enter
                logger.info(f"Clicked enter button for {email}")
            except Exception as e:
                logger.error(f"Error clicking enter button for {email}: {e}")
                raise
            
            # Step 4: Click all newsletter links (no duplicates, sequential)
            newsletter_links = [
                ("Fox Business Breaking News", 2),
                ("Fox Business Breaking News", 3),
                ("Fox News First Get all the", 2),
                ("Fox News First Get all the", 3),
                ("Antisemitism Exposed Fox News", 2),
                ("Fox News Politics Get the", 2),
                ("Fox News Politics Get the", 3),
                ("Fox Business Rundown Get a", 2),
                ("Fox Business Rundown Get a", 3),
                ("Fox News Entertainment Get a", 2),
                ("Fox News Entertainment Get a", 3),
                ("Fox True Crime The hottest", 2),
                ("Best of Opinion Get the recap", 2),
                ("Best of Opinion Get the recap", 3),
                ("Fox News Lifestyle A look at", 2),
                ("Fox News Lifestyle A look at", 3),
                ("Fox News Health Stay up-to-", 2),
                ("Fox News Health Stay up-to-", 3),
                ("Fox News Sports Huddle", 2),
                ("Fox News Sports Huddle", 3),
            ]
            
            for text, link_index in newsletter_links:
                try:
                    listitem = page.get_by_role("listitem").filter(has_text=text)
                    link = listitem.get_by_role("link").nth(link_index)
                    await link.wait_for(state='visible', timeout=5000)
                    await link.scroll_into_view_if_needed()
                    await page.wait_for_timeout(300)
                    await link.click()
                    await page.wait_for_timeout(1000)  # Wait 1 second between clicks
                    logger.info(f"Clicked newsletter link '{text}' nth({link_index}) for {email}")
                except Exception as e:
                    logger.warning(f"Error clicking newsletter link '{text}' nth({link_index}) for {email}: {e}")
                    continue
            
            # Step 5: Click Subscribe links sequentially
            subscribe_link_sequence = [1, 1, 1, 1, 2, 3, 1]  # Sequential clicks without duplicates
            
            for nth_index in subscribe_link_sequence:
                try:
                    subscribe_link = page.get_by_role("link", name="Subscribe").nth(nth_index)
                    await subscribe_link.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(500)  # Wait before clicking
                    await subscribe_link.scroll_into_view_if_needed()
                    await page.wait_for_timeout(300)
                    await subscribe_link.click()
                    await page.wait_for_timeout(1000)  # Wait 1 second between clicks
                    logger.info(f"Clicked Subscribe link nth({nth_index}) for {email}")
                except Exception as e:
                    logger.warning(f"Error clicking Subscribe link nth({nth_index}) for {email}: {e}")
                    continue
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to Fox newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to Fox: {e}")
            raise

