import { logger } from '../config.js';

const EMAIL_PATTERN = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

/**
 * Validate email address
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if email is valid
 */
export function isValidEmail(email) {
    if (!email || typeof email !== 'string') {
        return false;
    }
    return EMAIL_PATTERN.test(email.trim());
}

/**
 * Parse emails from text (comma-separated or newline-separated)
 * @param {string} text - Text containing emails
 * @returns {string[]} - Array of valid email addresses
 */
export function parseEmails(text) {
    if (!text || typeof text !== 'string') {
        return [];
    }
    
    const emails = [];
    // Handle both comma-separated and newline-separated emails
    const lines = text.trim().split(/[,\n]/);
    
    for (const line of lines) {
        const email = line.trim();
        if (email && isValidEmail(email)) {
            emails.push(email);
        }
    }
    
    logger.info(`Parsed ${emails.length} valid email(s) from input`);
    return emails;
}

