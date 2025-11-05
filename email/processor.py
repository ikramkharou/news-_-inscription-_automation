import asyncio
import logging
from typing import List
from playwright.async_api import async_playwright
from core.base_scraper import BaseScraper
from factory.scraper_factory import ScraperFactory
from config import EMAIL_PROCESSING_DELAY

logger = logging.getLogger(__name__)


class EmailProcessor:
    def __init__(self):
        self.scraper_factory = ScraperFactory()
    
    async def process_emails(self, url: str, emails: List[str], headless: bool = False) -> dict:
        results = {
            "total": len(emails),
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        scraper_class = self.scraper_factory.get_scraper_class(url)
        if not scraper_class:
            error_msg = f"Unsupported website URL: {url}"
            results["errors"].append(error_msg)
            logger.error(error_msg)
            return results
        
        
        async with async_playwright() as playwright:
            scraper = scraper_class()
            
            for email in emails:
                try:
                    await scraper.process_email(email, playwright, headless=headless)
                    results["success"] += 1
                    await asyncio.sleep(EMAIL_PROCESSING_DELAY)
                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Failed to process {email}: {str(e)}"
                    results["errors"].append(error_msg)
                    logger.error(error_msg)
        
        logger.info(f"Processing complete: {results['success']} success, {results['failed']} failed")
        return results

