#!/usr/bin/env python3
"""
Configuration loader that handles both .env files and config files
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

def load_config() -> Dict[str, Any]:
    """
    Load configuration from both .env file and config file
    .env file takes precedence for sensitive data
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Load base configuration
    with open('news_monitor_config.json', 'r') as f:
        config = json.load(f)
    
    # Override with environment variables if they exist
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        config['telegram']['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if os.getenv('TELEGRAM_CHAT_ID'):
        config['telegram']['chat_id'] = os.getenv('TELEGRAM_CHAT_ID')
    
    if os.getenv('NEWS_API_KEY'):
        config['news_apis']['news_api_key'] = os.getenv('NEWS_API_KEY')
    
    if os.getenv('ALPHA_VANTAGE_KEY'):
        config['news_apis']['alpha_vantage_key'] = os.getenv('ALPHA_VANTAGE_KEY')
    
    return config

def get_telegram_config() -> Dict[str, str]:
    """Get just the Telegram configuration"""
    config = load_config()
    return config['telegram']

if __name__ == "__main__":
    # Test the configuration loader
    config = load_config()
    print("Configuration loaded successfully!")
    print(f"Bot token present: {'Yes' if config['telegram']['bot_token'] != 'YOUR_BOT_TOKEN_HERE' else 'No'}")
    print(f"Chat ID present: {'Yes' if config['telegram']['chat_id'] != 'YOUR_CHAT_ID_HERE' else 'No'}")