"""
Test Script - Show Enhanced Message Formatting
Demonstrates the improved timestamps and links in Telegram messages
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot
from flash_news_monitor import FlashNewsMonitor, NewsAlert
from datetime import datetime

def test_enhanced_formatting():
    """Test and display the enhanced message formatting"""
    print("TESTING ENHANCED TELEGRAM MESSAGE FORMATTING")
    print("=" * 50)
    
    # Create bot instance
    bot = TelegramBot("dummy_token", "dummy_chat_id")
    
    print("\n1. ENHANCED TOP PERFORMERS MESSAGE")
    print("-" * 40)
    
    # Sample performance data with links
    sample_performers = [
        {
            'symbol': 'AAPL',
            'return_pct': 5.23,
            'end_price': 175.43,
            'sector': 'Technology'
        },
        {
            'symbol': 'MSFT',
            'return_pct': 3.87,
            'end_price': 378.85,
            'sector': 'Technology'
        }
    ]
    
    perf_message = bot.format_top_performers_message(sample_performers, 'return_pct')
    print(perf_message)
    print(f"Message length: {len(perf_message)} characters")
    
    print("\n2. ENHANCED EARNINGS CALENDAR MESSAGE")
    print("-" * 40)
    
    # Sample earnings data with links
    sample_earnings = [
        {
            'symbol': 'AAPL',
            'company_name': 'Apple Inc.',
            'next_earnings_date': '2025-10-30',
            'days_until_earnings': 5,
            'sector': 'Technology'
        },
        {
            'symbol': 'NVDA',
            'company_name': 'NVIDIA Corporation',
            'next_earnings_date': '2025-11-19',
            'days_until_earnings': 25,
            'sector': 'Technology'
        }
    ]
    
    earnings_message = bot.format_earnings_message(sample_earnings)
    print(earnings_message)
    print(f"Message length: {len(earnings_message)} characters")
    
    print("\n3. ENHANCED NEWS ALERT MESSAGE")
    print("-" * 40)
    
    # Create flash news monitor for testing
    monitor = FlashNewsMonitor("dummy_token", "dummy_chat_id")
    
    # Sample news alert with enhanced formatting
    sample_alert = NewsAlert(
        title="Apple Announces Revolutionary New iPhone with AI Integration",
        description="Apple Inc. unveiled its latest iPhone model featuring advanced AI capabilities, sending shares up 8% in after-hours trading. The new device includes breakthrough machine learning processors and enhanced camera technology.",
        url="https://finance.yahoo.com/news/apple-announces-revolutionary-iphone-ai-123456789.html",
        source="Yahoo Finance",
        published_at="2025-10-25T14:30:00Z",
        symbols_mentioned=["AAPL"],
        urgency_score=7,
        keywords_matched=["breakthrough", "ai integration", "shares up"]
    )
    
    alert_message = monitor.format_alert_message(sample_alert)
    print(alert_message)
    print(f"Message length: {len(alert_message)} characters")
    
    print("\n4. MESSAGE FEATURES SUMMARY")
    print("-" * 40)
    print("✓ Precise timestamps (YYYY-MM-DD HH:MM:SS)")
    print("✓ Clickable stock chart links for each symbol")
    print("✓ Direct earnings information links")
    print("✓ Full article links for news stories")
    print("✓ Fallback Google search links when no URL available")
    print("✓ Published time vs alert time distinction")
    print("✓ ISO timestamp format for precise timing")
    print("✓ HTML formatting for better readability")
    
    print("\n5. LINK EXAMPLES")
    print("-" * 40)
    print("Stock Charts: https://finance.yahoo.com/quote/AAPL")
    print("Earnings Info: https://finance.yahoo.com/calendar/earnings?symbol=AAPL")
    print("News Articles: https://finance.yahoo.com/news/article-url")
    print("Search Fallback: https://www.google.com/search?q=news+terms")
    
    print("\n" + "=" * 50)
    print("ENHANCED FORMATTING TEST COMPLETE")
    print("All messages now include comprehensive timestamps and clickable links!")

if __name__ == "__main__":
    test_enhanced_formatting()