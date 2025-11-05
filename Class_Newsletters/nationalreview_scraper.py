import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class NationalReviewScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://link.nationalreview.com/join/4rc/newdesign-nls-signup"
    
    async def subscribe_email(self, page: Page, email: str):
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                logger.info(f"Starting subscription attempt {attempt + 1} for {email} to National Review")
                
                # Step 1: Click checkbox 4
                try:
                    checkbox = page.locator("div:nth-child(4) > .checkbox > .checkmark")
                    await checkbox.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(1000)
                    await checkbox.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)
                    await checkbox.click()
                    await page.wait_for_timeout(1000)
                    logger.info(f"Clicked checkbox 4 for {email}")
                except Exception as e:
                    logger.warning(f"Error clicking checkbox 4 for {email}: {e}")
                
                # Step 2: Fill email and click SIGN UP
                try:
                    email_input = page.get_by_role("textbox", name="Email Address")
                    await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(1000)
                    await email_input.click()
                    await email_input.fill(email)
                    await page.wait_for_timeout(1000)
                    logger.info(f"Filled email address for {email}")
                    
                    signup_button = page.get_by_role("button", name="SIGN UP")
                    await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(1000)
                    await signup_button.click()
                    await page.wait_for_timeout(2000)  # Wait after clicking SIGN UP
                    logger.info(f"Clicked SIGN UP button for {email}")
                except Exception as e:
                    logger.warning(f"Error in first email/SIGN UP step for {email}: {e}")
                
                # Step 3: Click all checkboxes (first, then 2-9)
                try:
                    checkboxes_to_click = [
                        ".checkmark",  # first
                        "div:nth-child(2) > .checkbox > .checkmark",
                        "div:nth-child(3) > .checkbox > .checkmark",
                        "div:nth-child(4) > .checkbox > .checkmark",
                        "div:nth-child(5) > .checkbox > .checkmark",
                        "div:nth-child(6) > .checkbox > .checkmark",
                        "div:nth-child(7) > .checkbox > .checkmark",
                        "div:nth-child(8) > .checkbox > .checkmark",
                        "div:nth-child(9) > .checkbox > .checkmark",
                    ]
                    
                    for checkbox_selector in checkboxes_to_click:
                        try:
                            if checkbox_selector == ".checkmark":
                                checkbox = page.locator(checkbox_selector).first
                            else:
                                checkbox = page.locator(checkbox_selector)
                            
                            await checkbox.wait_for(state='visible', timeout=5000)
                            await checkbox.scroll_into_view_if_needed()
                            await page.wait_for_timeout(300)
                            await checkbox.click()
                            await page.wait_for_timeout(500)
                            logger.info(f"Clicked checkbox {checkbox_selector} for {email}")
                        except Exception as e:
                            logger.warning(f"Error clicking checkbox {checkbox_selector} for {email}: {e}")
                            continue
                except Exception as e:
                    logger.warning(f"Error clicking checkboxes for {email}: {e}")
                
                # Step 4: Fill email again
                try:
                    email_input = page.get_by_role("textbox", name="Email Address")
                    await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(1000)
                    await email_input.click()
                    await email_input.fill(email)
                    await page.wait_for_timeout(1000)
                    logger.info(f"Filled email address again for {email}")
                except Exception as e:
                    logger.warning(f"Error filling email again for {email}: {e}")
                
                # Check if we're done or need to retry
                await page.wait_for_timeout(3000)
                
                # If this is the last attempt or we think we succeeded, break
                if attempt == max_attempts - 1:
                    logger.info(f"Completed all {max_attempts} attempts for {email}")
                    break
                
                # Wait a bit before retrying
                await page.wait_for_timeout(2000)
                
            except Exception as e:
                logger.error(f"Error in attempt {attempt + 1} for {email}: {e}")
                if attempt == max_attempts - 1:
                    # Last attempt failed, close browser
                    logger.error(f"All attempts failed for {email}, closing browser")
                    raise
        
        await page.wait_for_timeout(5000)
        logger.info(f"Subscribed {email} to National Review newsletters")

