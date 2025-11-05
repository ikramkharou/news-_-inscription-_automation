import logging
import re
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class PennLiveScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://link.pennlive.com/join/6fl/signup"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to PennLive")
            
            # Set up dialog handler to dismiss any dialogs (only once)
            async def handle_dialog(dialog):
                await dialog.dismiss()
            page.once("dialog", handle_dialog)
            
            # Click all newsletter subscription buttons with 1 second waits between clicks
            newsletter_clicks = [
                (".listing-button", "first", None),
                ("div:nth-child(2) > .newsletterlist__listings--listing-checkbox-label > .listing-button", None, None),
                ("div:nth-child(3) > .newsletterlist__listings--listing-checkbox-label > .listing-button", None, None),
                ("div:nth-child(4) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(5) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(6) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(7) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(8) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(9) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(10) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(11) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(12) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(13) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div", "filter_regex", r"^News at Noon Noon weekdaysYour look at the top headlines as of midday\.$"),
                ("div", "filter_regex", r"^Evening News 6 p\.m\. weekdaysYour after-work recap of the top headlines\.$"),
                ("div:nth-child(16) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(17) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(18) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(19) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(20) > .newsletterlist__listings--listing-checkbox-label > .listing-button", None, None),
                ("div:nth-child(21) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div:nth-child(22) > .newsletterlist__listings--listing-checkbox-label > .listing-button > .button-icon", None, None),
                ("div", "filter_regex_label", r"^PennLive Exclusives 8 a\.m\. SundaysStories you'll find only from PennLive\.$"),
                ("div", "filter_regex", r"^PennLive Real Deals OccasionalSpecial offers from our advertising partners\.$"),
            ]
            
            for selector, modifier, pattern in newsletter_clicks:
                try:
                    if modifier == "first":
                        element = page.locator(selector).first
                    elif modifier == "filter_regex":
                        element = page.locator("div").filter(has_text=re.compile(pattern)).locator("span").nth(2)
                    elif modifier == "filter_regex_label":
                        element = page.locator("div").filter(has_text=re.compile(pattern)).locator("label div")
                    else:
                        element = page.locator(selector)
                    
                    await element.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await element.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)  # Wait for scroll
                    await element.click()
                    await page.wait_for_timeout(1000)  # Wait 1 second between clicks
                except Exception as e:
                    logger.warning(f"Error clicking newsletter button '{selector}' for {email}: {e}")
                    continue
            
            # Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Email")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking email field
                await email_input.click()
                await email_input.fill(email)
                await page.wait_for_timeout(1000)  # Wait after filling email
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Click Sign Up button
            try:
                signup_button = page.locator('input#form-submit[type="submit"][value="Sign Up"]')
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking Sign Up
                await signup_button.click()
                logger.info(f"Clicked Sign Up button for {email}")
                await page.wait_for_timeout(3000)  # Wait for confirmation
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Sign Up button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to PennLive newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to PennLive: {e}")
            raise

