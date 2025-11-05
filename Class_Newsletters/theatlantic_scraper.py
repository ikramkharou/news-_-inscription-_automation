import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class TheAtlanticScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.theatlantic.com/newsletters/"
    
    async def subscribe_email(self, page: Page, email: str):
        try:

            logger.info(f"Starting subscription for {email} to The Atlantic")
            
            # Click newsletter subscription items - all use paragraph.nth(1)
            newsletter_clicks = [
                "Weekday MorningsThe Atlantic",
                "Weekday Evenings and Sunday",
                "At least once a weekTrump's",
                "Weekday and Sunday",
                "Sunday EveningsThis WeekAn",
                "As editor's notes are",
                "Thursday MorningsHow to Build",
                "WeeklyThe Weekly PlanetThe",
                "WeeklyWork in ProgressDerek",
                "WeeklyBeing HumanOur health",
                "As new articles are publishedGalaxy BrainA newsletter from Charlie Warzel about",
                "As new articles are publishedDeep ShtetlYair Rosenberg demystifies the often",
                "Every TuesdayDear JamesIn his",
                "WeeklyAtlantic",
                "As new photo essays are",
                "WeeklyTime-Travel",
            ]
            
            # Click all newsletter items using paragraph.nth(1)
            for text in newsletter_clicks:
                try:
                    # Try to find the listitem with a shorter timeout, then retry if needed
                    listitem = page.get_by_role("listitem").filter(has_text=text)
                    try:
                        await listitem.wait_for(state='visible', timeout=5000)
                    except Exception as timeout_error:
                        # If exact match fails, try partial match
                        if "timeout" in str(timeout_error).lower():
                            logger.warning(f"Exact match timed out for '{text}', trying partial match for {email}")
                            listitem = page.get_by_role("listitem").filter(has_text=text[:30] if len(text) > 30 else text)
                            await listitem.wait_for(state='visible', timeout=5000)
                        else:
                            raise
                    
                    # Scroll the listitem into view first
                    await listitem.scroll_into_view_if_needed()
                    await page.wait_for_timeout(1000)  # Wait for animations to settle
                    
                    # All items use paragraph.nth(1) according to the new sequence
                    element = listitem.get_by_role("paragraph").nth(1)
                    await element.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    
                    # Try normal click first, if it fails due to interception, use force
                    try:
                        await element.click(timeout=5000)
                        # Wait a bit to see if "Selected" appears
                        await page.wait_for_timeout(1000)
                        # Check if the newsletter is now selected
                        try:
                            selected_indicator = listitem.locator("div.NewsletterCard_buttonIcon__gCltK p.NewsletterCard_iconText__y8nhU")
                            if await selected_indicator.count() > 0:
                                selected_text = await selected_indicator.first.inner_text()
                                if "Selected" in selected_text:
                                    logger.info(f"Newsletter '{text}' successfully selected for {email}")
                        except:
                            pass
                    except Exception as click_error:
                        if "intercepts pointer events" in str(click_error) or "intercepted" in str(click_error).lower():
                            logger.warning(f"Click intercepted for '{text}', trying force click for {email}")
                            await element.click(force=True)
                            await page.wait_for_timeout(1000)
                        else:
                            raise
                    
                    await page.wait_for_timeout(1000)  # Wait 1 second between clicks
                except Exception as e:
                    logger.warning(f"Error clicking newsletter item '{text}' for {email}: {e}")
                    continue
            
            # Click "Select" buttons (multiple clicks at the end)
            try:
                # First 4 clicks use .first
                for i in range(4):
                    select_button = page.get_by_text("Select", exact=True).first
                    await select_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await page.wait_for_timeout(1000)  # Wait before clicking
                    await select_button.click()
                    await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                    logger.info(f"Clicked Select button {i+1} (first) for {email}")
                
                # Last click without .first
                select_button = page.get_by_text("Select", exact=True)
                await select_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(1000)  # Wait before clicking
                await select_button.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds after clicking
                logger.info(f"Clicked Select button 5 (no first) for {email}")
            except Exception as e:
                logger.warning(f"Error clicking Select buttons for {email}: {e}")
            
            # Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Email Address")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(3000)  # Wait before clicking email field
                await email_input.click()
                await page.wait_for_timeout(3000)  # Wait after clicking, before filling
                await email_input.fill(email)
                await page.wait_for_timeout(3000)  # Wait after filling email
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Click Sign Up button
            try:
                signup_button = page.get_by_role("button", name="Sign Up")
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await page.wait_for_timeout(3000)  # Wait before clicking Sign Up
                await signup_button.click()
                logger.info(f"Clicked Sign Up button for {email}")
                await page.wait_for_timeout(3000)  # Wait after clicking Sign Up
                logger.info(f"Waiting for confirmation message for {email}")
            except Exception as e:
                logger.error(f"Error clicking Sign Up button for {email}: {e}")
                raise
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to The Atlantic newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to The Atlantic: {e}")
            raise

