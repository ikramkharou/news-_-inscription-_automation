import winston from 'winston';

export const PROXY_FILE = "250 proxies (1).txt";
export const DEFAULT_HEADLESS = false;
export const EMAIL_PROCESSING_DELAY = 2; // seconds
export const BROWSER_TIMEOUT = 10000; // milliseconds

export const SUPPORTED_SITES = {
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
};

// Configure logger
export const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
            return `${timestamp} - ${level.toUpperCase()} - ${message} ${Object.keys(meta).length ? JSON.stringify(meta) : ''}`;
        })
    ),
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.printf(({ timestamp, level, message, ...meta }) => {
                    return `${timestamp} - ${level} - ${message} ${Object.keys(meta).length ? JSON.stringify(meta) : ''}`;
                })
            )
        })
    ]
});

