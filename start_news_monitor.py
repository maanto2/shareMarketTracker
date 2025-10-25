"""
Quick Start Script for Flash News Monitor
Simple interface to start monitoring news
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flash_news_monitor import FlashNewsMonitor
from config_loader import load_config
import time

def quick_start():
    """Quick start monitoring with default settings"""
    print("FLASH NEWS MONITOR - QUICK START")
    print("=" * 40)
    
    # Load config
    config = load_config()
    if not config:
        print("Could not load configuration file")
        return
    
    # Extract settings
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']
    news_api_key = config['news_apis'].get('news_api_key')
    check_interval = config['monitoring']['check_interval_minutes']
    
    # Create monitor
    monitor = FlashNewsMonitor(bot_token, chat_id, news_api_key)
    
    # Add symbols from config
    symbols = config['monitoring']['symbols_to_monitor']
    monitor.monitored_symbols = set(symbols)
    
    print(f"Configured to monitor {len(monitor.monitored_symbols)} symbols")
    print(f"Check interval: {check_interval} minutes")
    print(f"Telegram chat ID: {chat_id}")
    
    # Start monitoring
    try:
        print("\nStarting news monitoring...")
        print("Press Ctrl+C to stop")
        
        monitor.start_monitoring(interval_minutes=check_interval)
        
        # Keep running
        while monitor.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop_monitoring()
        print("Monitor stopped.")

if __name__ == "__main__":
    quick_start()