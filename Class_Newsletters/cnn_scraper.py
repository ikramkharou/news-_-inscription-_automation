import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class CNNScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://edition.cnn.com/newsletters"

    async def subscribe_email(self, page: Page, email: str):
        try:

            # Implement the subscription logic for CNN
            await page.pause()
            
            button = page.locator('xpath=/html/body/div[3]/div/a')
            try:
                await button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                if await button.is_visible():
                    await button.click()
                    logger.info(f"Clicked navigation start button for {email}")
            except Exception:
                logger.info(f"Navigation button not visible for {email}, proceeding to select buttons directly")
            
        

            clicked_count = 0
            for i in range(2):
                try:
                    newsletter_locator = page.locator(f"#newsletter-{i}").get_by_role("button", name="Select")
                    await newsletter_locator.click()
                    clicked_count += 1
                    logger.info(f"Clicked newsletter-{i} button for {email}")
                except Exception as e:
                    logger.debug(f"Newsletter-{i} button not found or not clickable")
                    continue
            
            try:
                newsletter_empty = page.locator("#newsletter-").get_by_role("button", name="Select")
                await newsletter_empty.click()
                clicked_count += 1
                logger.info(f"Clicked newsletter- button for {email}")
            except Exception as e:
                logger.debug(f"Newsletter- button not found or not clickable")

            logger.info(f"Successfully clicked {clicked_count} newsletter buttons for {email}")
            


            #fill email address and click sign up button
            try:
                email_input = page.get_by_role("textbox", name="Email address")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await email_input.fill(email)
                logger.info(f"Filled email address field for {email}")
                
                signup_button = page.get_by_role("button", name="Sign Up", exact=True)
                await signup_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await signup_button.click()
                logger.info(f"Clicked Sign Up button for {email}")
            except Exception as e:
                logger.error(f"Error filling email or clicking Sign Up for {email}: {e}")
                raise
            


            #click start puzzle button for Arkose Labs captcha
            try:
                await page.wait_for_timeout(3000)
                
                start_puzzle_clicked = False
                
                try:
                    verification_frame = page.frame_locator("iframe[title=\"Verification challenge\"]")
                    visual_frame = verification_frame.frame_locator("iframe[title=\"Visual challenge\"]")
                    
                    start_puzzle_button = visual_frame.locator('xpath=/html/body/div/div/div[1]/button')
                    try:
                        await start_puzzle_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                        if await start_puzzle_button.is_visible():
                            await start_puzzle_button.click()
                            logger.info(f"Clicked Start Puzzle button (xpath method) for {email}")
                            start_puzzle_clicked = True
                    except Exception:
                        logger.debug(f"Start Puzzle button not visible (xpath method) for {email}")
                except Exception as e:
                    logger.debug(f"Failed to find Start Puzzle button with xpath method: {e}")
                
                if not start_puzzle_clicked:
                    try:
                        dialog = page.get_by_role("dialog")
                        verification_frame = dialog.locator("iframe[title=\"Verification challenge\"]").content_frame()
                        visual_frame = verification_frame.locator("iframe[title=\"Visual challenge\"]").content_frame()
                        
                        start_puzzle_button = visual_frame.get_by_role("button", name="Start Puzzle")
                        await start_puzzle_button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                        await start_puzzle_button.click()
                        logger.info(f"Clicked Start Puzzle button (get_by_role method) for {email}")



                        
                    except Exception as e:
                        logger.warning(f"Failed to click Start Puzzle button with get_by_role method: {e}")
            except Exception as e:
                logger.warning(f"Captcha handling failed for {email}: {e}")
            
            await page.wait_for_timeout(50000)
            logger.info(f"Subscribed {email} to CNN newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to CNN: {e}")
            raise

