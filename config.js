const boolFromEnv = (key, fallback = false) => {
    const val = process.env[key];
    if (val === undefined) return fallback;
    return ["1", "true", "yes", "y"].includes(val.toString().trim().toLowerCase());
};

const numberFromEnv = (key, fallback) => {
    const val = process.env[key];
    if (val === undefined) return fallback;
    const n = Number(val);
    return Number.isFinite(n) ? n : fallback;
};

// Configuration strictly sourced from environment (no hardcoded defaults)
export const PROXY_FILE = process.env.PROXY_FILE;
export const PROXY_URL = process.env.PROXY_URL;
export const DEFAULT_HEADLESS = boolFromEnv("HEADLESS");
export const EMAIL_PROCESSING_DELAY = numberFromEnv("EMAIL_PROCESSING_DELAY"); // seconds
export const BROWSER_TIMEOUT = numberFromEnv("BROWSER_TIMEOUT"); // milliseconds

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

// Simple logger replacement for desktop usage
export const logger = {
    info: (...args) => console.log('[INFO]', ...args),
    warn: (...args) => console.warn('[WARN]', ...args),
    error: (...args) => console.error('[ERROR]', ...args)
};

