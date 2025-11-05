import re
import logging

logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

#validate email address
def is_valid_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))

#parse emails from text
def parse_emails(text: str) -> list:
    if not text or not isinstance(text, str):
        return []
    
    emails = []
    for line in text.strip().split('\n'):
        email = line.strip()
        if email and is_valid_email(email):
            emails.append(email)
    
    logger.info(f"Parsed {len(emails)} valid email(s) from input")
    return emails

