from core.base_scraper import BaseScraper
from .cnn_scraper import CNNScraper
from .fox_scraper import FoxScraper
from .theatlantic_scraper import TheAtlanticScraper
from .theverge_scraper import TheVergeScraper
from .vox_scraper import VoxScraper
from .apnews_scraper import APNewsScraper
from .nationalreview_scraper import NationalReviewScraper
from .axios_scraper import AxiosScraper
from .pennlive_scraper import PennLiveScraper
from .theguardian_scraper import TheGuardianScraper
from .techcrunch_scraper import TechCrunchScraper
from .quartz_scraper import QuartzScraper

__all__ = [
    'BaseScraper', 'CNNScraper', 'FoxScraper', 'TheAtlanticScraper', 'TheVergeScraper',
    'VoxScraper', 'APNewsScraper', 'NationalReviewScraper', 'AxiosScraper',
    'PennLiveScraper', 'TheGuardianScraper', 'TechCrunchScraper', 'QuartzScraper'
]

