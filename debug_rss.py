#!/usr/bin/env python3
"""
Debug RSS feed parsing
"""

import requests
import re
from datetime import datetime

def debug_rss_feed(url):
    print(f"Testing RSS feed: {url}")
    print("=" * 50)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Content length: {len(content)} characters")
            
            # Show first 500 characters
            print("\nFirst 500 characters of response:")
            print("-" * 30)
            print(content[:500])
            print("-" * 30)
            
            # Try to find items
            items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
            print(f"\nFound {len(items)} items using regex")
            
            if items:
                print("\nFirst item:")
                print(items[0][:300] + "..." if len(items[0]) > 300 else items[0])
                
                # Test parsing
                item = items[0]
                title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
                desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
                link_match = re.search(r'<link>(.*?)</link>', item)
                
                print(f"\nTitle match: {title_match.group(1) if title_match else 'Not found'}")
                print(f"Description match: {desc_match.group(1)[:100] if desc_match else 'Not found'}")
                print(f"Link match: {link_match.group(1) if link_match else 'Not found'}")
            
            # Alternative: look for entry tags (Atom format)
            entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
            print(f"\nAlso found {len(entries)} entries using <entry> tags")
            
        else:
            print(f"Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test different URLs
    test_urls = [
        'https://feeds.finance.yahoo.com/rss/2.0/headline',
        'https://feeds.marketwatch.com/marketwatch/realtimeheadlines/',
        'https://www.cnbc.com/id/100003114/device/rss/rss.html'
    ]
    
    for url in test_urls:
        debug_rss_feed(url)
        print("\n" + "="*80 + "\n")