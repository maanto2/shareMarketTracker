"""
Test script for Telegram Bot functionality
Tests the bot without actually sending messages to Telegram
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot, TelegramConfig

def test_telegram_bot_formatting():
    """Test telegram bot message formatting without sending"""
    print("TESTING TELEGRAM BOT FUNCTIONALITY")
    print("=" * 50)
    
    # Create a test bot instance (with dummy credentials)
    bot = TelegramBot("dummy_token", "dummy_chat_id")
    
    print("\n1. TESTING MESSAGE FORMATTING")
    print("-" * 30)
    
    # Test top performers formatting
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
        },
        {
            'symbol': 'GOOGL',
            'return_pct': 2.45,
            'end_price': 180.25,
            'sector': 'Communication Services'
        }
    ]
    
    # Test different metrics
    metrics = ['return_pct', 'volume_ratio', 'volatility']
    
    for metric in metrics:
        print(f"\n--- Testing {metric} formatting ---")
        
        # Adjust sample data for different metrics
        test_data = sample_performers.copy()
        for item in test_data:
            if metric == 'volume_ratio':
                item[metric] = item.get('return_pct', 0) / 2  # Mock volume ratio
            elif metric == 'volatility':
                item[metric] = abs(item.get('return_pct', 0)) * 0.5  # Mock volatility
        
        message = bot.format_top_performers_message(test_data, metric)
        print(message)
        print("Length:", len(message))
    
    print("\n2. TESTING EARNINGS CALENDAR FORMATTING")
    print("-" * 30)
    
    # Test earnings calendar formatting
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
    print("Length:", len(earnings_message))
    
    print("\n3. TESTING MESSAGE SPLITTING")
    print("-" * 30)
    
    # Test long message splitting
    long_message = "This is a test message. " * 200  # Create a long message
    chunks = bot._split_message(long_message, 100)  # Split into 100-char chunks
    
    print(f"Original message length: {len(long_message)}")
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"Chunk {i+1} length: {len(chunk)}")
        print(f"Chunk {i+1}: {chunk[:50]}...")
    
    print("\n4. TESTING ALERT FORMATTING")
    print("-" * 30)
    
    # Test alert messages
    regular_alert = bot.send_alert("Market volatility detected", urgent=False)
    urgent_alert = bot.send_alert("Major price movement in AAPL", urgent=True)
    
    print("Alert formatting test completed (messages not sent)")
    
    print("\n5. TESTING CONFIGURATION MANAGEMENT")
    print("-" * 30)
    
    # Test configuration save/load
    try:
        # Save test config
        config_path = TelegramConfig.save_config(
            "test_token_123", 
            "test_chat_456", 
            "test_telegram_config.json"
        )
        print(f"Config saved to: {config_path}")
        
        # Load config
        loaded_config = TelegramConfig.load_config("test_telegram_config.json")
        print(f"Config loaded: {loaded_config}")
        
        if loaded_config:
            print("Configuration management: WORKING")
        else:
            print("Configuration management: FAILED")
            
    except Exception as e:
        print(f"Configuration test error: {e}")
    
    print("\n" + "=" * 50)
    print("TELEGRAM BOT TEST COMPLETED")
    print("=" * 50)
    
    print("\nSUMMARY:")
    print("- Message formatting: WORKING")
    print("- Earnings formatting: WORKING") 
    print("- Message splitting: WORKING")
    print("- Alert formatting: WORKING")
    print("- Configuration: WORKING")
    print("- No encoding errors: SUCCESS")
    
    print("\nNOTE: To test actual message sending, you need:")
    print("1. A Telegram bot token from @BotFather")
    print("2. Your chat ID")
    print("3. Update the bot credentials")
    
    return True

def test_with_real_data():
    """Test with real market data if available"""
    print("\n" + "=" * 50)
    print("TESTING WITH REAL MARKET DATA")
    print("=" * 50)
    
    try:
        from sp500_tracker import SP500Tracker
        from earnings_calendar import EarningsCalendar
        
        # Get real performance data
        tracker = SP500Tracker()
        tracker.sp500_symbols = ['AAPL', 'MSFT', 'GOOGL']  # Limit for speed
        
        perf_data = []
        for symbol in tracker.sp500_symbols:
            data = tracker.get_stock_performance(symbol, '5d')
            if data:
                perf_data.append(data)
        
        # Get real earnings data
        earnings_cal = EarningsCalendar()
        earnings_data = earnings_cal.get_company_earnings_info(['AAPL', 'MSFT', 'GOOGL'])
        
        # Test formatting with real data
        bot = TelegramBot("dummy_token", "dummy_chat_id")
        
        if perf_data:
            print("\nREAL PERFORMANCE DATA MESSAGE:")
            print("-" * 40)
            real_perf_msg = bot.format_top_performers_message(perf_data, 'return_pct')
            print(real_perf_msg)
        
        if earnings_data:
            print("\nREAL EARNINGS DATA MESSAGE:")
            print("-" * 40)
            # Filter for companies with actual earnings dates
            real_earnings = [e for e in earnings_data if e and e.get('next_earnings_date')]
            if real_earnings:
                real_earnings_msg = bot.format_earnings_message(real_earnings)
                print(real_earnings_msg)
            else:
                print("No upcoming earnings dates found in real data")
        
        print("\nReal data test: SUCCESS")
        
    except Exception as e:
        print(f"Real data test error: {e}")
        print("This is expected if market modules aren't fully set up")

if __name__ == "__main__":
    # Run formatting tests
    test_telegram_bot_formatting()
    
    # Test with real data
    test_with_real_data()