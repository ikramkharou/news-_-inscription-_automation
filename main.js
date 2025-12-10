import { logger, DEFAULT_HEADLESS } from './config.js';
import { EmailProcessor } from './email-utils/processor.js';
import { ScraperFactory } from './factory/scraper-factory.js';
import { parseEmails } from './email-utils/validator.js';

logger.info("Starting Newsletter Subscription Tool");

function parseBool(value, fallback = false) {
    if (value === undefined || value === null) return fallback;
    const normalized = value.toString().trim().toLowerCase();
    return ["1", "true", "yes", "y"].includes(normalized);
}

function parseArgs(argv = process.argv.slice(2)) {
    const args = { email: undefined, url: undefined, headless: undefined };
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        const next = argv[i + 1];
        if ((arg === "--email" || arg === "-e") && next) {
            args.email = next;
            i++;
        } else if ((arg === "--url" || arg === "-u") && next) {
            args.url = next;
            i++;
        } else if ((arg === "--headless" || arg === "-h") && next !== undefined) {
            args.headless = next;
            i++;
        }
    }
    return args;
}

function gatherInput() {
    const cli = parseArgs();
    const rawEmails = cli.email ?? process.env.EMAILS ?? "";
    const url = cli.url ?? process.env.URL ?? process.env.SITE_URL ?? "";
    const headless = parseBool(cli.headless ?? process.env.HEADLESS, DEFAULT_HEADLESS);
    return { rawEmails, url, headless };
}

async function run() {
    const { rawEmails, url, headless } = gatherInput();

    const emails = parseEmails(rawEmails);
    if (!emails.length) {
        logger.error("No valid email addresses found. Provide --email or EMAILS (comma/newline separated).");
        process.exit(1);
    }

    if (!url) {
        logger.error("Missing URL. Provide --url or URL/SITE_URL env.");
        process.exit(1);
    }

    if (!ScraperFactory.isSupportedUrl(url)) {
        const supported = ScraperFactory.getSupportedSitesList();
        logger.error(`Unsupported website URL: ${url}`);
        logger.error(`Supported sites: ${supported}`);
        process.exit(1);
    }

    try {
        logger.info(`Processing ${emails.length} email(s) for URL: ${url} (headless=${headless})`);
        const emailProcessor = new EmailProcessor();
        const results = await emailProcessor.processEmails(url, emails, headless);

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
        process.exit(results.failed > 0 ? 1 : 0);
    } catch (error) {
        logger.error(`Fatal error: ${error.message}`);
        process.exit(1);
    }
}

run();

