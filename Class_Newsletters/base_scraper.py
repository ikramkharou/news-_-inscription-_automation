import logging
import random
from abc import ABC, abstractmethod
from playwright.async_api import Playwright, Page
from config import PROXY_FILE, DEFAULT_HEADLESS, BROWSER_TIMEOUT

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(self, proxy_file: str = PROXY_FILE):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()
    
    def _load_proxies(self):
        try:
            proxies = []
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) == 4:
                            ip, port, username, password = parts
                            proxies.append({
                                "server": f"http://{ip}:{port}",
                                "username": username,
                                "password": password
                            })
            logger.info(f"Loaded {len(proxies)} proxies")
            return proxies
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
            return []
    
    def _get_random_proxy(self):
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    async def _launch_browser(self, playwright: Playwright, headless: bool = DEFAULT_HEADLESS):
        chromium = playwright.chromium
        proxy = self._get_random_proxy()
        
        launch_options = {"headless": headless}
        if proxy:
            launch_options["proxy"] = proxy
            logger.info(f"Launching browser with proxy: {proxy['server']} (headless={headless})")
        else:
            logger.warning(f"No proxy available, launching browser without proxy (headless={headless})")
        
        browser = await chromium.launch(**launch_options)
        logger.info("Browser launched successfully")
        return browser
    
    @abstractmethod
    def get_url(self) -> str:
        pass
    
    @abstractmethod
    async def subscribe_email(self, page: Page, email: str):
        pass
    
    async def process_email(self, email: str, playwright: Playwright):
        browser = None
        try:
            browser = await self._launch_browser(playwright)
            page = await browser.new_page()
            await page.goto(self.get_url())
            
            await self.subscribe_email(page, email)
            
            await browser.close()
            logger.info(f"Successfully processed email: {email}")
        except Exception as e:
            logger.error(f"Error processing email {email}: {e}")
            if browser:
                await browser.close()

