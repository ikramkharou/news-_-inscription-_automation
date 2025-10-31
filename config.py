import logging

PROXY_FILE = "250 proxies (1).txt"
DEFAULT_HEADLESS = False
EMAIL_PROCESSING_DELAY = 2
BROWSER_TIMEOUT = 10000

SUPPORTED_SITES = {
    "CNN": ["cnn.com", "edition.cnn.com"],
    "Fox News": ["foxnews.com", "fox.com"],
    "The Atlantic": ["theatlantic.com"],
    "The Verge": ["theverge.com"],
    "Vox": ["vox.com"],
    "AP News": ["apnews.com"],
    "National Review": ["nationalreview.com"],
    "Axios": ["axios.com"],
    "PennLive": ["pennlive.com"],
    "The Guardian": ["theguardian.com"],
    "TechCrunch": ["techcrunch.com"],
    "Quartz": ["qz.com"]
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

