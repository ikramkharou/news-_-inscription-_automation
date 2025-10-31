import logging
from typing import Optional, Type
from Class_Newsletters.base_scraper import BaseScraper
from Class_Newsletters.cnn_scraper import CNNScraper
from Class_Newsletters.fox_scraper import FoxScraper
from Class_Newsletters.theatlantic_scraper import TheAtlanticScraper
from Class_Newsletters.theverge_scraper import TheVergeScraper
from Class_Newsletters.vox_scraper import VoxScraper
from Class_Newsletters.apnews_scraper import APNewsScraper
from Class_Newsletters.nationalreview_scraper import NationalReviewScraper
from Class_Newsletters.axios_scraper import AxiosScraper
from Class_Newsletters.pennlive_scraper import PennLiveScraper
from Class_Newsletters.theguardian_scraper import TheGuardianScraper
from Class_Newsletters.techcrunch_scraper import TechCrunchScraper
from Class_Newsletters.quartz_scraper import QuartzScraper
from config import SUPPORTED_SITES

logger = logging.getLogger(__name__)


class ScraperFactory:
    _scraper_map = {
        "CNN": CNNScraper,
        "Fox News": FoxScraper,
        "The Atlantic": TheAtlanticScraper,
        "The Verge": TheVergeScraper,
        "Vox": VoxScraper,
        "AP News": APNewsScraper,
        "National Review": NationalReviewScraper,
        "Axios": AxiosScraper,
        "PennLive": PennLiveScraper,
        "The Guardian": TheGuardianScraper,
        "TechCrunch": TechCrunchScraper,
        "Quartz": QuartzScraper
    }
    
    @classmethod
    def create_scraper(cls, url: str) -> Optional[BaseScraper]:
        scraper_class = cls.get_scraper_class(url)
        if scraper_class:
            return scraper_class()
        return None
    
    @classmethod
    def get_scraper_class(cls, url: str) -> Optional[Type[BaseScraper]]:
        if not url:
            return None
        
        url_lower = url.lower().strip()
        
        for site_name, domains in SUPPORTED_SITES.items():
            for domain in domains:
                if domain in url_lower:
                    scraper_class = cls._scraper_map.get(site_name)
                    if scraper_class:
                        logger.info(f"Matched URL '{url}' to {site_name} scraper")
                        return scraper_class
        
        logger.warning(f"No scraper found for URL: {url}")
        return None
    
    @classmethod
    def is_supported_url(cls, url: str) -> bool:
        return cls.get_scraper_class(url) is not None
    
    @classmethod
    def get_supported_sites_list(cls) -> str:
        return ", ".join(SUPPORTED_SITES.keys())

