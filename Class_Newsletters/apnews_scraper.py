import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class APNewsScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://apnews.com/newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to AP News")
            
            # Step 1: Click checkbox labels (first, then 2-6)
            checkbox_selectors = [
                ".checkbox-label",  # first
                "div:nth-child(2) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(3) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(4) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(5) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
                "div:nth-child(6) > .NewsletterItem > .NewsletterItem-content > .NewsletterItem-checkbox > span > .checkbox-label",
            ]
            
            for selector in checkbox_selectors:
                try:
                    if selector == ".checkbox-label":
                        checkbox = page.locator(selector).first
                    else:
                        checkbox = page.locator(selector)
                    
                    await checkbox.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await checkbox.scroll_into_view_if_needed()
                    await page.wait_for_timeout(300)
                    await checkbox.click()
                    await page.wait_for_timeout(1000)  # Wait 1 second between clicks
                    logger.info(f"Clicked checkbox {selector} for {email}")
                except Exception as e:
                    logger.warning(f"Error clicking checkbox {selector} for {email}: {e}")
                    continue
            
            # Step 2: Click SELECT buttons multiple times
            # First 3 clicks use .first
            for i in range(3):
                try:
                    select_button = page.get_by_text("SELECT", exact=True).first
                    await select_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(500)
                    await select_button.click()
                    await page.wait_for_timeout(1000)
                    logger.info(f"Clicked SELECT button (first) - click {i+1} for {email}")
                except Exception as e:
                    logger.warning(f"Error clicking SELECT button (first) - click {i+1} for {email}: {e}")
            
            # Click "Enable accessibility" text
            try:
                enable_accessibility = page.get_by_text("Enable accessibility0 .st0{")
                await enable_accessibility.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(500)
                await enable_accessibility.click()
                await page.wait_for_timeout(1000)
                logger.info(f"Clicked Enable accessibility for {email}")
            except Exception as e:
                logger.warning(f"Error clicking Enable accessibility for {email}: {e}")
            
            # Click SELECT button first one more time
            try:
                select_button = page.get_by_text("SELECT", exact=True).first
                await select_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(500)
                await select_button.click()
                await page.wait_for_timeout(1000)
                logger.info(f"Clicked SELECT button (first) again for {email}")
            except Exception as e:
                logger.warning(f"Error clicking SELECT button (first) again for {email}: {e}")
            
            # Click SELECT button without .first
            try:
                select_button = page.get_by_text("SELECT", exact=True)
                await select_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(500)
                await select_button.click()
                await page.wait_for_timeout(1000)
                logger.info(f"Clicked SELECT button (no first) for {email}")
            except Exception as e:
                logger.warning(f"Error clicking SELECT button (no first) for {email}: {e}")
            
            # Step 3: Fill email address (ensure clean and valid)
            try:
                email_input = page.get_by_role("textbox", name="Share your email here")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking email field
                
                # Click the field to focus
                await email_input.click()
                await page.wait_for_timeout(500)
                
                # Clear any existing content by selecting all and deleting
                # Use keyboard shortcut to select all (works cross-platform)
                await email_input.press("Control+a")  # Select all
                await page.wait_for_timeout(200)
                await email_input.press("Delete")  # Delete selected content
                await page.wait_for_timeout(300)
                
                # Clean the email (trim whitespace)
                clean_email = email.strip()
                
                # Validate email format (basic check)
                if "@" not in clean_email or "." not in clean_email.split("@")[-1]:
                    logger.warning(f"Email format may be invalid: {clean_email}")
                else:
                    logger.info(f"Email format validated: {clean_email}")
                
                # Fill with clean email (fill method automatically clears and types)
                await email_input.fill(clean_email)
                await page.wait_for_timeout(500)  # Wait after filling
                
                # Press Tab to trigger email validation
                await email_input.press("Tab")
                await page.wait_for_timeout(2000)  # Wait for validation to complete
                
                # Wait for any validation errors to clear
                await page.wait_for_timeout(1000)  # Additional wait to ensure validation is complete
                logger.info(f"Filled email address field with clean email: {clean_email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Step 4: Click disclaimer checkbox
            try:
                disclaimer_checkbox = page.get_by_role("main").locator("div").filter(has_text="Newsletters Selected Please provide a valid email address, and check disclaimer").locator("label").nth(1)
                await disclaimer_checkbox.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking
                await disclaimer_checkbox.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await disclaimer_checkbox.click()
                await page.wait_for_timeout(2000)  # Wait longer after clicking checkbox
                logger.info(f"Clicked disclaimer checkbox for {email}")
            except Exception as e:
                logger.warning(f"Error clicking disclaimer checkbox for {email}: {e}")
            
            # Step 5: Click submit button (wait longer to ensure email is validated)
            try:
                submit_button = page.locator("#Newsletter-Banner-submitBtn")
                await submit_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(2000)  # Wait longer before clicking submit to ensure validation
                await submit_button.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await submit_button.click()
                logger.info(f"Clicked submit button for {email}")
                await page.wait_for_timeout(3000)  # Wait for confirmation
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking submit button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to AP News newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to AP News: {e}")
            raise

