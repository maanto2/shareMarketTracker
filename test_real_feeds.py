#!/usr/bin/env python3
"""
Test script to verify real RSS feeds are working with proper URLs and sources
"""

from flash_news_monitor import FlashNewsMonitor
from config_loader import load_config

def test_real_feeds():
    print("Testing Flash News Monitor with Real RSS Feeds")
    print("=" * 50)
    
    # Create monitor instance with config
    config = load_config()
    
    monitor = FlashNewsMonitor(
        bot_token=config['telegram']['bot_token'],
        chat_id=config['telegram']['chat_id']
    )
    
    print("Getting real news alerts...")
    alerts = monitor.get_all_news()
    
    if alerts:
        print(f"\nFound {len(alerts)} real news alerts:")
        print("-" * 50)
        
        for i, alert in enumerate(alerts[:3], 1):  # Show first 3
            print(f"\nAlert {i}:")
            print(f"Title: {alert.title}")
            print(f"Source: {alert.source}")
            print(f"URL: {alert.url}")
            print(f"Symbols: {', '.join(alert.symbols_mentioned)}")
            print(f"Urgency: {alert.urgency_score}/10")
            print(f"Published: {alert.published_at}")
            print("-" * 50)
            
    else:
        print("No real news alerts found. Testing RSS feeds directly...")
        
        # Test individual RSS feeds
        test_urls = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',
            'https://feeds.marketwatch.com/marketwatch/realtimeheadlines/',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html'
        ]
        
        for url in test_urls:
            print(f"\nTesting RSS feed: {url}")
            articles = monitor.get_news_from_rss(url)
            if articles:
                print(f"Found {len(articles)} articles")
                article = articles[0]  # Show first article
                print(f"Title: {article['title']}")
                print(f"URL: {article['url']}")
                print(f"Source: {article['source']}")
            else:
                print("No articles found")

if __name__ == "__main__":
    test_real_feeds()