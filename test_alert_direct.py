#!/usr/bin/env python3
"""
Direct test of flash news monitor test alerts
"""

from flash_news_monitor import FlashNewsMonitor
from config_loader import load_config

def test_alert_system():
    print("Testing Flash News Monitor Alert System")
    print("=" * 50)
    
    # Create monitor instance with config
    config = load_config()
    
    monitor = FlashNewsMonitor(
        bot_token=config['telegram']['bot_token'],
        chat_id=config['telegram']['chat_id']
    )
    
    # Run the test alert function directly
    print("Running test alert system...")
    monitor.test_alert_system()

if __name__ == "__main__":
    test_alert_system()