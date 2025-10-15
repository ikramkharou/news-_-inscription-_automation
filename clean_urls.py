#!/usr/bin/env python3
"""
Clean URL file to contain only domain names, one per line
"""

import re
from urllib.parse import urlparse

def clean_urls(input_file, output_file):
    """Clean URLs to contain only domain names"""
    
    clean_domains = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, headers, and metadata
        if not line or line.startswith('=') or line.startswith('TOP') or line.startswith('Scraped') or line.startswith('Date') or line.startswith('Total'):
            continue
        
        # Extract URL from line (handle formats like "4. https://example.com/" or just "https://example.com/")
        url_match = re.search(r'https?://[^\s]+', line)
        if url_match:
            url = url_match.group(0)
            
            try:
                # Parse URL to extract domain
                parsed = urlparse(url)
                domain = parsed.netloc
                
                # Remove www. prefix if present
                if domain.startswith('www.'):
                    domain = domain[4:]
                
                # Only add if domain is not empty and not already in list
                if domain and domain not in clean_domains:
                    clean_domains.append(domain)
                    
            except Exception as e:
                print(f"Error parsing URL '{url}': {e}")
                continue
    
    # Write clean domains to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for domain in clean_domains:
            f.write(domain + '\n')
    
    print(f"✅ Cleaned {len(clean_domains)} domains")
    print(f"📁 Saved to: {output_file}")
    
    # Show first few domains as example
    print(f"\n📋 First 10 domains:")
    for i, domain in enumerate(clean_domains[:10], 1):
        print(f"  {i}. {domain}")
    
    if len(clean_domains) > 10:
        print(f"  ... and {len(clean_domains) - 10} more")

if __name__ == "__main__":
    input_file = "shopify_stores_20251013_192215.txt"
    output_file = "clean_domains.txt"
    
    print("🧹 Cleaning URL file to contain only domain names...")
    clean_urls(input_file, output_file)
    print("✅ URL cleaning completed!")
