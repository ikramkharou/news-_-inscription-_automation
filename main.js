import { Command } from 'commander';
import { logger } from './config.js';
import { EmailProcessor } from './email-utils/processor.js';
import { ScraperFactory } from './factory/scraper-factory.js';
import { parseEmails, isValidEmail } from './email-utils/validator.js';

logger.info("Starting Newsletter Subscription Tool");

const program = new Command();

program
    .name('newsletter-subscription')
    .description('Newsletter Subscription Tool - Command Line Interface')
    .version('1.0.0');

program
    .requiredOption('-e, --email <emails>', 'Email address(es) to subscribe (can be single email or comma-separated list)')
    .requiredOption('-u, --url <url>', 'Website URL to subscribe to')
    .option('-h, --headless <true|false>', 'Run browser in headless mode (true/false). Default: false', 'false')
    .action(async (options) => {
        try {
            // Parse emails
            const emails = parseEmails(options.email);
            if (!emails || emails.length === 0) {
                logger.error("No valid email addresses found. Please provide a valid email.");
                process.exit(1);
            }
            
            // Validate URL
            if (!ScraperFactory.isSupportedUrl(options.url)) {
                const supported = ScraperFactory.getSupportedSitesList();
                logger.error(`Unsupported website URL: ${options.url}`);
                logger.error(`Supported sites: ${supported}`);
                process.exit(1);
            }
            
            // Parse headless flag
            const headless = options.headless.toLowerCase() === "true";
            
            logger.info(`Processing ${emails.length} email(s) for URL: ${options.url} (headless=${headless})`);
            
            // Process emails
            const emailProcessor = new EmailProcessor();
            const results = await emailProcessor.processEmails(options.url, emails, headless);
            
            // Log results
            logger.info("=".repeat(50));
            logger.info("PROCESSING RESULTS");
            logger.info("=".repeat(50));
            logger.info(`Total emails: ${results.total}`);
            logger.info(`Success: ${results.success}`);
            logger.info(`Failed: ${results.failed}`);
            
            if (results.errors && results.errors.length > 0) {
                logger.error(`Errors (${results.errors.length}):`);
                const errorsToShow = results.errors.slice(0, 10);
                for (const error of errorsToShow) {
                    logger.error(`  - ${error}`);
                }
                if (results.errors.length > 10) {
                    logger.error(`  ... and ${results.errors.length - 10} more errors`);
                }
            }
            
            logger.info("=".repeat(50));
            
            // Exit with error code if any failed
            if (results.failed > 0) {
                process.exit(1);
            } else {
                process.exit(0);
            }
        } catch (error) {
            logger.error(`Fatal error: ${error.message}`);
            process.exit(1);
        }
    });

program.parse();

