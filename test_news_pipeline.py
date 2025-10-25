#!/usr/bin/env python3
"""
Test the complete news alert pipeline
"""

from flash_news_monitor import FlashNewsMonitor
from config_loader import load_config

def test_news_pipeline():
    print("Testing Complete News Alert Pipeline")
    print("=" * 50)
    
    # Create monitor instance with config
    config = load_config()
    
    monitor = FlashNewsMonitor(
        bot_token=config['telegram']['bot_token'],
        chat_id=config['telegram']['chat_id']
    )
    
    print("Getting all RSS news...")
    all_articles = []
    
    # Test each RSS feed
    for i, rss_url in enumerate(monitor.news_sources):
        print(f"\nTesting RSS feed {i+1}: {rss_url}")
        articles = monitor.get_news_from_rss(rss_url)
        print(f"Found {len(articles)} articles")
        
        if articles:
            print(f"Sample article:")
            article = articles[0]
            print(f"  Title: {article['title'][:80]}...")
            print(f"  Source: {article['source']}")
            
            # Test symbol extraction
            text = article['title'] + ' ' + article['description']
            symbols = monitor.extract_symbols_from_text(text)
            print(f"  Symbols found: {symbols}")
            
            if symbols:
                urgency = monitor.calculate_urgency_score(
                    article['title'], 
                    article['description'], 
                    symbols
                )
                print(f"  Urgency score: {urgency}")
                print(f"  Would create alert: YES")
            else:
                print(f"  Would create alert: NO (no relevant symbols)")
        
        all_articles.extend(articles)
    
    print(f"\nTotal articles collected: {len(all_articles)}")
    
    # Now test the complete pipeline
    print("\n" + "="*50)
    print("Testing complete get_all_news() pipeline...")
    alerts = monitor.get_all_news()
    print(f"Final alerts created: {len(alerts)}")
    
    for i, alert in enumerate(alerts[:3], 1):
        print(f"\nAlert {i}:")
        print(f"  Title: {alert.title}")
        print(f"  Source: {alert.source}")
        print(f"  URL: {alert.url}")
        print(f"  Symbols: {', '.join(alert.symbols_mentioned)}")
        print(f"  Urgency: {alert.urgency_score}/10")

if __name__ == "__main__":
    test_news_pipeline()