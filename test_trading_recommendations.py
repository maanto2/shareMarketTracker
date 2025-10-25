#!/usr/bin/env python3
"""
Test BUY/SELL Trading Recommendations
Shows how sentiment analysis generates trading recommendations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sentiment_analyzer import SentimentAnalyzer
from telegram_bot import TelegramBot
from config_loader import load_config
from datetime import datetime

def test_trading_recommendations():
    """Test the trading recommendation system"""
    print("🎯 TESTING BUY/SELL TRADING RECOMMENDATIONS")
    print("=" * 60)
    
    # Load config
    config = load_config()
    
    # Create sentiment analyzer (with or without NewsAPI)
    news_api_key = config['news_apis'].get('news_api_key')
    analyzer = SentimentAnalyzer(news_api_key)
    
    # Test different sentiment scenarios
    test_scenarios = [
        {
            'sentiment': 'positive',
            'score': 2.5,
            'confidence': 85.0,
            'description': 'Strong positive earnings beat with high confidence'
        },
        {
            'sentiment': 'positive',
            'score': 0.8,
            'confidence': 75.0,
            'description': 'Moderate positive outlook with good confidence'
        },
        {
            'sentiment': 'negative',
            'score': -2.1,
            'confidence': 80.0,
            'description': 'Strong negative news with high confidence'
        },
        {
            'sentiment': 'negative',
            'score': -0.7,
            'confidence': 65.0,
            'description': 'Moderate negative sentiment'
        },
        {
            'sentiment': 'positive',
            'score': 1.2,
            'confidence': 45.0,
            'description': 'Positive but low confidence'
        },
        {
            'sentiment': 'neutral',
            'score': 0.1,
            'confidence': 30.0,
            'description': 'Mixed/unclear sentiment'
        }
    ]
    
    print("Testing Trading Recommendation Logic:")
    print("-" * 40)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario['description']}")
        print(f"Sentiment: {scenario['sentiment']}, Score: {scenario['score']}, Confidence: {scenario['confidence']}%")
        
        # Generate recommendation
        rec = analyzer._generate_trading_recommendation(
            scenario['sentiment'], 
            scenario['score'], 
            scenario['confidence']
        )
        
        # Format output
        action = rec['action']
        strength = rec['strength']
        reason = rec['reason']
        
        # Add emoji
        if action == 'BUY':
            if strength == 'STRONG':
                emoji = "🟢🟢"
            elif strength == 'MODERATE':
                emoji = "🟢"
            else:
                emoji = "🟡"
        elif action == 'SELL':
            if strength == 'STRONG':
                emoji = "🔴🔴"
            elif strength == 'MODERATE':
                emoji = "🔴"
            else:
                emoji = "🟠"
        else:
            emoji = "⚪"
        
        print(f"→ Recommendation: {emoji} {strength} {action}")
        print(f"→ Reason: {reason}")
    
    # Test sample earnings with recommendations
    print("\n" + "=" * 60)
    print("🗓️ SAMPLE EARNINGS CALENDAR WITH RECOMMENDATIONS")
    print("=" * 60)
    
    # Create sample data
    sample_earnings = [
        {
            'symbol': 'AAPL',
            'company_name': 'Apple Inc.',
            'next_earnings_date': '2025-10-30',
            'days_until_earnings': 5,
            'sector': 'Technology'
        },
        {
            'symbol': 'MSFT',
            'company_name': 'Microsoft Corporation',
            'next_earnings_date': '2025-10-29',
            'days_until_earnings': 4,
            'sector': 'Technology'
        }
    ]
    
    sample_sentiment = [
        {
            'symbol': 'AAPL',
            'overall_sentiment': 'positive',
            'overall_score': 1.8,
            'confidence': 78.0,
            'trading_recommendation': analyzer._generate_trading_recommendation('positive', 1.8, 78.0)
        },
        {
            'symbol': 'MSFT',
            'overall_sentiment': 'negative',
            'overall_score': -1.2,
            'confidence': 72.0,
            'trading_recommendation': analyzer._generate_trading_recommendation('negative', -1.2, 72.0)
        }
    ]
    
    # Create telegram bot and format message
    telegram_bot = TelegramBot(
        config['telegram']['bot_token'],
        config['telegram']['chat_id']
    )
    
    # Format earnings message with recommendations
    earnings_message = telegram_bot.format_earnings_message(sample_earnings, sample_sentiment)
    
    print("Sample Telegram Message with BUY/SELL Recommendations:")
    print("-" * 50)
    print(earnings_message)
    
    # Test news alert recommendations
    print("\n" + "=" * 60)
    print("📰 SAMPLE NEWS ALERT WITH TRADING RECOMMENDATION")
    print("=" * 60)
    
    from flash_news_monitor import NewsAlert, FlashNewsMonitor
    
    # Create a sample news alert
    sample_alert = NewsAlert(
        title="Apple Reports Record Q4 Earnings, Beats Wall Street Expectations",
        description="Apple Inc. posted strong quarterly results with iPhone sales surging 15% and services revenue hitting new highs, significantly beating analyst expectations.",
        url="https://finance.yahoo.com/news/apple-earnings-beat-expectations",
        source="Yahoo Finance",
        published_at=datetime.now().isoformat(),
        symbols_mentioned=["AAPL"],
        urgency_score=8,
        keywords_matched=["earnings beat", "exceeds expectations", "record quarterly"]
    )
    
    # Create monitor to format the alert
    monitor = FlashNewsMonitor(
        config['telegram']['bot_token'],
        config['telegram']['chat_id']
    )
    
    alert_message = monitor.format_alert_message(sample_alert)
    
    print("Sample News Alert with Trading Assessment:")
    print("-" * 50)
    print(alert_message)
    
    print("\n✅ Trading Recommendation Testing Complete!")
    print("\nThe system now provides:")
    print("• 📊 BUY/SELL recommendations for earnings calendar")
    print("• 🎯 Quick trading assessments for breaking news")
    print("• 📈 Strength indicators (STRONG, MODERATE, WEAK)")
    print("• 🔍 Confidence-based filtering")

if __name__ == "__main__":
    test_trading_recommendations()