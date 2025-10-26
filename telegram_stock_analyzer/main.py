#!/usr/bin/env python3
"""
Main Runner for Interactive Telegram Stock Analyzer
Starts the bot and handles configuration
"""

import json
import os
from datetime import datetime
from interactive_telegram_bot import InteractiveTelegramBot

def load_config():
    """Load configuration from file or create template"""
    config_file = "telegram_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return None
    else:
        # Create template config file
        template_config = {
            "bot_token": "YOUR_BOT_TOKEN_HERE",
            "authorized_chat_ids": [
                "YOUR_CHAT_ID_HERE"
            ],
            "news_api_key": None,
            "created": datetime.now().isoformat(),
            "instructions": {
                "bot_token": "Get this from @BotFather on Telegram",
                "authorized_chat_ids": "List of Telegram chat IDs allowed to use the bot",
                "news_api_key": "Optional: Get from newsapi.org for enhanced news analysis"
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(template_config, f, indent=2)
            
            print(f"📄 Created template config file: {config_file}")
            print("🔧 Please edit the config file with your Telegram bot token and chat ID")
            return None
        except Exception as e:
            print(f"❌ Error creating config file: {e}")
            return None

def validate_config(config):
    """Validate configuration"""
    if not config:
        return False
    
    # Check required fields
    bot_token = config.get('bot_token')
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your bot_token in telegram_config.json")
        print("   Get your token from @BotFather on Telegram")
        return False
    
    authorized_chat_ids = config.get('authorized_chat_ids', [])
    if not authorized_chat_ids or "YOUR_CHAT_ID_HERE" in authorized_chat_ids:
        print("❌ Please set your authorized_chat_ids in telegram_config.json")
        print("   Add your Telegram chat ID to the list")
        return False
    
    return True

def get_chat_id_instructions():
    """Show instructions for getting chat ID"""
    instructions = """
📱 HOW TO GET YOUR TELEGRAM CHAT ID:

1️⃣ Start a chat with @userinfobot on Telegram
2️⃣ Send any message to the bot
3️⃣ The bot will reply with your chat ID
4️⃣ Copy the ID number (it will look like: 123456789)
5️⃣ Add it to the authorized_chat_ids list in telegram_config.json

📝 Example config:
{
  "bot_token": "1234567890:ABCdefGhIjKlMnOpQrStUvWxYz",
  "authorized_chat_ids": ["123456789"],
  ...
}

💡 You can also add multiple chat IDs to allow multiple users.
"""
    return instructions

def main():
    """Main function"""
    print("🤖 TELEGRAM STOCK ANALYZER")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    if not config:
        print("\n" + get_chat_id_instructions())
        return
    
    # Validate configuration
    if not validate_config(config):
        print("\n" + get_chat_id_instructions())
        return
    
    # Extract configuration
    bot_token = config['bot_token']
    authorized_chat_ids = config.get('authorized_chat_ids', [])
    news_api_key = config.get('news_api_key')
    
    print(f"✅ Configuration loaded successfully")
    print(f"🔑 Bot token: {bot_token[:10]}..." if bot_token else "❌ No bot token")
    print(f"👥 Authorized users: {len(authorized_chat_ids)}")
    print(f"📰 News API: {'✅ Available' if news_api_key else '❌ Not configured (using free sources)'}")
    
    try:
        # Create and start bot
        print("\n🚀 Starting Telegram Stock Analyzer Bot...")
        bot = InteractiveTelegramBot(bot_token, authorized_chat_ids)
        
        # Pass news API key to the stock analyzer if available
        if news_api_key:
            bot.stock_analyzer.news_api_key = news_api_key
        
        print("✅ Bot initialized successfully!")
        print("\n📱 READY TO ANALYZE STOCKS!")
        print("=" * 30)
        print("💬 Send a stock symbol to your bot on Telegram")
        print("📊 Example: AAPL, TSLA, MSFT, GOOGL")
        print("🎯 Commands: /help, /status")
        print("⏹️  Press Ctrl+C to stop")
        print("=" * 30)
        
        # Start the bot
        bot.start_bot()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Check your bot token is correct")
        print("2. Ensure your chat ID is in the authorized list")
        print("3. Make sure your bot has the necessary permissions")
        print("4. Check your internet connection")
    
    print("\n👋 Telegram Stock Analyzer terminated")

if __name__ == "__main__":
    main()