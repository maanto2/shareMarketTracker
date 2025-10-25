#!/usr/bin/env python3
"""
Show what the current test alerts look like
"""

from flash_news_monitor import FlashNewsMonitor, NewsAlert
from config_loader import load_config
from datetime import datetime

def show_current_alerts():
    print("Current Test Alert Format")
    print("=" * 50)
    
    # Create the same realistic test alerts that the system uses
    test_alerts = [
        NewsAlert(
            title="S&P 500 Hits New Record High on Strong Earnings Reports",
            description="The S&P 500 index reached a new all-time high as major technology companies reported better-than-expected quarterly earnings, boosting investor confidence in the market.",
            url="https://finance.yahoo.com/news/sp-500-record-high-earnings-reports",
            source="Yahoo Finance",
            published_at=datetime.now().isoformat(),
            symbols_mentioned=["SPY", "AAPL", "MSFT"],
            urgency_score=6,
            keywords_matched=["record high", "strong earnings"]
        ),
        NewsAlert(
            title="Federal Reserve Officials Signal Potential Rate Changes Ahead",
            description="Federal Reserve officials indicated in recent speeches that interest rate adjustments may be considered based on upcoming economic data and inflation trends.",
            url="https://finance.yahoo.com/news/federal-reserve-rate-changes-ahead",
            source="Yahoo Finance",
            published_at=datetime.now().isoformat(),
            symbols_mentioned=["SPY"],
            urgency_score=8,
            keywords_matched=["federal reserve", "interest rate"]
        )
    ]
    
    # Create monitor instance to use the formatting function
    config = load_config()
    
    monitor = FlashNewsMonitor(
        bot_token=config['telegram']['bot_token'],
        chat_id=config['telegram']['chat_id']
    )
    
    for i, alert in enumerate(test_alerts, 1):
        print(f"\nTest Alert {i}:")
        print(f"Title: {alert.title}")
        print(f"Source: {alert.source}")
        print(f"URL: {alert.url}")
        print(f"Symbols: {', '.join(alert.symbols_mentioned)}")
        
        # Show the formatted message
        formatted_message = monitor.format_alert_message(alert)
        print(f"\nFormatted Telegram Message:")
        print("-" * 30)
        print(formatted_message)
        print("-" * 30)

if __name__ == "__main__":
    show_current_alerts()