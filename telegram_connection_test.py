"""
Quick Telegram Bot Connection Test
Use this to test actual message sending with your bot credentials
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot
from config_loader import load_config

def test_telegram_connection():
    """Test actual Telegram bot connection and message sending"""
    print("TELEGRAM BOT CONNECTION TEST")
    print("=" * 40)
    
    # Load credentials from config
    try:
        config = load_config()
        BOT_TOKEN = config['telegram']['bot_token']
        CHAT_ID = config['telegram']['chat_id']
    except Exception as e:
        print(f"ERROR: Could not load configuration: {e}")
        print("Make sure your .env file is set up correctly")
        return False
    
    # Quick check if credentials are set
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("SETUP REQUIRED:")
        print("1. Create a .env file with your credentials")
        print("2. Copy .env.example to .env")
        print("3. Edit .env with your bot token and chat ID")
        print("4. Run this test again")
        print("\nSee CONFIG_SETUP.md for detailed instructions")
        return False
    
    # Create bot instance
    try:
        bot = TelegramBot(BOT_TOKEN, CHAT_ID)
        print(f"Bot initialized with token: {BOT_TOKEN[:10]}...")
        
        # Test basic connection
        print("\nTesting connection...")
        if bot.test_connection():
            print("SUCCESS: Bot connection working!")
            
            # Test market update message
            print("\nTesting market update message...")
            
            # Sample data
            sample_performers = [
                {
                    'symbol': 'AAPL',
                    'return_pct': 2.5,
                    'end_price': 262.82,
                    'sector': 'Technology'
                },
                {
                    'symbol': 'MSFT', 
                    'return_pct': 1.8,
                    'end_price': 523.61,
                    'sector': 'Technology'
                }
            ]
            
            sample_earnings = [
                {
                    'symbol': 'AAPL',
                    'company_name': 'Apple Inc.',
                    'next_earnings_date': '2025-10-30',
                    'days_until_earnings': 5,
                    'sector': 'Technology'
                }
            ]
            
            # Send market update
            success = bot.send_market_update(
                top_performers=sample_performers,
                earnings_data=sample_earnings,
                metric='return_pct'
            )
            
            if success:
                print("SUCCESS: Market update sent!")
            else:
                print("WARNING: Market update failed to send")
            
            # Test alert
            alert_success = bot.send_alert("This is a test alert from your market analysis bot!")
            if alert_success:
                print("SUCCESS: Alert sent!")
            else:
                print("WARNING: Alert failed to send")
            
            return True
            
        else:
            print("FAILED: Bot connection test failed")
            print("Check your bot token and chat ID")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def setup_bot_instructions():
    """Print detailed setup instructions"""
    print("\nHOW TO SET UP YOUR TELEGRAM BOT:")
    print("=" * 50)
    print("1. Open Telegram and search for @BotFather")
    print("2. Start a chat with BotFather")
    print("3. Send /newbot command")
    print("4. Choose a name for your bot (e.g., 'My Market Bot')")
    print("5. Choose a username (must end with 'bot', e.g., 'mymarket_bot')")
    print("6. BotFather will give you a token like: 123456789:ABCdefGhiJklMnoPqrsTuvWxyz")
    print("7. Copy this token and paste it as BOT_TOKEN in this script")
    print("\n8. To get your Chat ID:")
    print("   - Search for @userinfobot on Telegram")
    print("   - Send /start to get your user ID")
    print("   - Copy the ID number and use as CHAT_ID")
    print("\n9. Update the credentials in this script and run again")

if __name__ == "__main__":
    # Test connection
    success = test_telegram_connection()
    
    if not success:
        setup_bot_instructions()
        
    print(f"\nTest completed: {'SUCCESS' if success else 'SETUP NEEDED'}")