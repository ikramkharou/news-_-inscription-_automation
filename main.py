import argparse
import asyncio
import sys
from email_utils import EmailProcessor, parse_emails
from factory.scraper_factory import ScraperFactory
from config import logger

logger.info("Starting Newsletter Subscription Tool")


def main():
    parser = argparse.ArgumentParser(
        description="Newsletter Subscription Tool - Command Line Interface"
    )
    
    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email address to subscribe (can be single email or comma-separated list)"
    )
    
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Website URL to subscribe to"
    )
    
    parser.add_argument(
        "--headless",
        type=str,
        default="false",
        choices=["true", "false", "True", "False", "TRUE", "FALSE"],
        help="Run browser in headless mode (true/false). Default: false"
    )
    
    args = parser.parse_args()
    
    # Parse emails
    emails = parse_emails(args.email)
    if not emails:
        logger.error("No valid email addresses found. Please provide a valid email.")
        sys.exit(1)
    
    # Validate URL
    scraper_factory = ScraperFactory()
    if not scraper_factory.is_supported_url(args.url):
        supported = scraper_factory.get_supported_sites_list()
        logger.error(f"Unsupported website URL: {args.url}")
        logger.error(f"Supported sites: {supported}")
        sys.exit(1)
    
    # Parse headless flag
    headless = args.headless.lower() == "true"
    
    logger.info(f"Processing {len(emails)} email(s) for URL: {args.url} (headless={headless})")
    
    # Process emails
    email_processor = EmailProcessor()
    results = asyncio.run(email_processor.process_emails(args.url, emails, headless=headless))
    
    # Log results
    logger.info("="*50)
    logger.info("PROCESSING RESULTS")
    logger.info("="*50)
    logger.info(f"Total emails: {results['total']}")
    logger.info(f"Success: {results['success']}")
    logger.info(f"Failed: {results['failed']}")
    
    if results.get("errors"):
        logger.error(f"Errors ({len(results['errors'])}):")
        for error in results["errors"][:10]:  # Show first 10 errors
            logger.error(f"  - {error}")
        if len(results["errors"]) > 10:
            logger.error(f"  ... and {len(results['errors']) - 10} more errors")
    
    logger.info("="*50)
    
    # Exit with error code if any failed
    if results['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

