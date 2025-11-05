import logging
from core.base_scraper import BaseScraper
from playwright.async_api import Page
from config import BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class TheGuardianScraper(BaseScraper):
    def get_url(self) -> str:
        return "https://www.theguardian.com/email-newsletters"
    
    async def subscribe_email(self, page: Page, email: str):
        try:
            logger.info(f"Starting subscription for {email} to The Guardian")
            
            # Click all newsletter subscription buttons
            newsletter_buttons = [
                "add Detox Your Kitchen to",
                "add This Week in Trumpland to",
                "add The Long Wave to",
                "add First Thing to subscribe",
                "add The Overwhelm to",
                "add Fighting Back to",
                "add Well Actually to",
                "add Reclaim your brain to",
                "add Trump on Trial to",
                "add Soccer with Jonathan",
                "add Down to Earth to",
                "add Follow Mehdi Hasan to",
                "add Follow Robert Reich to",
                "add Follow Margaret Sullivan",
                "add The Week in Patriarchy to",
                "add This is Europe to",
                "add TechScape to subscribe",
                "add Fashion Statement to",
                "add The Guide to subscribe",
                "add Film Weekly to subscribe",
                "add Sleeve Notes to subscribe",
                "add What's On to subscribe",
                "add Art Weekly to subscribe",
                "add Documentaries to",
                "add Inside Saturday to",
                "add Five Great Reads to",
                "add The Upside to subscribe",
                "add The Long Read to",
                "add Saved for Later to",
                "add House to Home to",
                "add Global Dispatch to",
                "add Cotton Capital to",
                "add The Traveller to",
                "add Her Stage to subscribe",
                "add The Crunch to subscribe",
                "add Football Daily to",
                "add Moving the Goalposts to",
                "add The Spin to subscribe list",
                "add The Breakdown to",
                "add The Recap to subscribe",
                "add Australia Sport to",
                "add Headlines US to subscribe",
                "add Opinion US to subscribe",
                "add Headlines UK to subscribe",
                "add Opinion UK to subscribe",
                "add Opinion AUS to subscribe",
                "add Headlines Europe to",
                "add Business Today to",
                "add Headlines AUS to",
                "add First Edition to",
                "add Saturday Edition to",
                "add Morning Mail to subscribe",
                "add Afternoon Update to",
                "add Australian Politics to"
            ]
            
            # Click all newsletter buttons with 3 second waits between clicks
            for button_name in newsletter_buttons:
                try:
                    button = page.get_by_role("button", name=button_name)
                    await button.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await button.click()
                    await page.wait_for_timeout(3000)  # Wait 3 seconds between clicks
                except Exception as e:
                    logger.warning(f"Error clicking newsletter button '{button_name}' for {email}: {e}")
                    continue
            
            # Fill email address
            try:
                email_input = page.get_by_role("textbox", name="Enter your email")
                await email_input.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await email_input.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds before filling
                await email_input.fill(email)
                await page.wait_for_timeout(3000)  # Wait 3 seconds after filling
                logger.info(f"Filled email address field for {email}")
            except Exception as e:
                logger.error(f"Error filling email address for {email}: {e}")
                raise
            
            # Uncheck and check the updates checkbox
            try:
                updates_checkbox = page.get_by_role("checkbox", name="Get updates about our")
                await updates_checkbox.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await updates_checkbox.check()
                await page.wait_for_timeout(3000)  # Wait 3 seconds
                logger.info(f"Toggled updates checkbox for {email}")
            except Exception as e:
                logger.warning(f"Error toggling updates checkbox for {email}: {e}")
            
            # Click reCAPTCHA checkbox in iframe
            try:
                iframe = page.locator("iframe[name=\"a-xhsigsb8cosx\"]")
                await iframe.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                frame = await iframe.content_frame()
                if frame:
                    recaptcha_checkbox = frame.get_by_role("checkbox", name="I'm not a robot")
                    await recaptcha_checkbox.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                    await recaptcha_checkbox.click()
                    await page.wait_for_timeout(3000)  # Wait 3 seconds
                    logger.info(f"Clicked reCAPTCHA checkbox for {email}")
            except Exception as e:
                logger.warning(f"Error clicking reCAPTCHA checkbox for {email}: {e}")
            
            # Click the final div element
            try:
                final_div = page.locator("div:nth-child(13) > div").first
                await final_div.wait_for(state='visible', timeout=BROWSER_TIMEOUT)
                await final_div.click()
                await page.wait_for_timeout(3000)  # Wait 3 seconds
                logger.info(f"Clicked final div element for {email}")
            except Exception as e:
                logger.warning(f"Error clicking final div element for {email}: {e}")
            
            await page.wait_for_timeout(5000)
            logger.info(f"Subscribed {email} to The Guardian newsletters")
        except Exception as e:
            logger.error(f"Error subscribing {email} to The Guardian: {e}")
            raise

