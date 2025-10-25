"""
Telegram Bot for Market Updates
Sends earnings dates and top performers data via Telegram
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram bot
        
        Args:
            bot_token: Your Telegram bot token from @BotFather
            chat_id: Your chat ID or channel ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message via Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result['ok']:
                print("Message sent successfully!")
                return True
            else:
                print(f"Error sending message: {result}")
                return False
                
        except Exception as e:
            print(f"Exception sending Telegram message: {e}")
            return False
    
    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        """Send a photo with caption via Telegram"""
        try:
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, files=files, data=data)
                result = response.json()
                
                if result['ok']:
                    print("Photo sent successfully!")
                    return True
                else:
                    print(f"Error sending photo: {result}")
                    return False
                    
        except Exception as e:
            print(f"Exception sending Telegram photo: {e}")
            return False
    
    def format_top_performers_message(self, performers_data: List[Dict], metric: str) -> str:
        """Format top performers data for Telegram message"""
        if not performers_data:
            return "No performance data available"
        
        # Symbol mapping for metrics
        symbol_map = {
            'return_pct': 'RETURNS',
            'volume_ratio': 'VOLUME',
            'volatility': 'VOLATILITY'
        }
        
        symbol = symbol_map.get(metric, 'PERFORMANCE')
        
        current_time = datetime.now()
        message = f"<b>TOP PERFORMERS - {metric.replace('_', ' ').upper()}</b>\n"
        message += f"<i>Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</i>\n\n"
        
        for i, company in enumerate(performers_data[:10], 1):
            symbol = company.get('symbol', 'N/A')
            value = company.get(metric, 0)
            price = company.get('end_price', 0)
            sector = company.get('sector', 'Unknown')
            
            # Format the metric value
            if metric == 'return_pct':
                metric_str = f"{value:+.2f}%"
            elif metric == 'volume_ratio':
                metric_str = f"{value:.2f}x"
            else:
                metric_str = f"{value:.2f}"
            
            # Create Yahoo Finance link for each stock
            yahoo_link = f"https://finance.yahoo.com/quote/{symbol}"
            
            message += f"{i:2d}. <b>{symbol}</b> | {metric_str} | ${price:.2f}\n"
            message += f"    <i>{sector}</i> | <a href='{yahoo_link}'>View Chart</a>\n\n"
        
        return message
    
    def format_earnings_message(self, earnings_data: List[Dict]) -> str:
        """Format earnings calendar data for Telegram message"""
        if not earnings_data:
            return "No upcoming earnings found"
        
        current_time = datetime.now()
        message = "<b>UPCOMING EARNINGS CALENDAR</b>\n"
        message += f"<i>Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</i>\n\n"
        
        for company in earnings_data:
            symbol = company.get('symbol', 'N/A')
            name = company.get('company_name', 'Unknown')
            date = company.get('next_earnings_date', 'N/A')
            days = company.get('days_until_earnings', 'N/A')
            sector = company.get('sector', 'Unknown')
            
            # Add priority indicator based on days until earnings
            if isinstance(days, int):
                if days <= 3:
                    priority = "[URGENT]"
                elif days <= 7:
                    priority = "[SOON]"
                else:
                    priority = ""
            else:
                priority = ""
            
            # Create links for each company
            yahoo_link = f"https://finance.yahoo.com/quote/{symbol}"
            earnings_link = f"https://finance.yahoo.com/calendar/earnings?symbol={symbol}"
            
            message += f"{priority} <b>{symbol}</b> - {name[:20]}\n"
            message += f"Date: {date}\n"
            
            if isinstance(days, int):
                message += f"In {days} days\n"
            
            message += f"Sector: {sector}\n"
            message += f"<a href='{yahoo_link}'>Stock Chart</a> | <a href='{earnings_link}'>Earnings Info</a>\n\n"
        
        return message
    
    def send_market_update(self, 
                          top_performers: List[Dict] = None,
                          earnings_data: List[Dict] = None,
                          metric: str = 'return_pct') -> bool:
        """Send comprehensive market update"""
        
        messages = []
        
        # Top performers message
        if top_performers:
            perf_message = self.format_top_performers_message(top_performers, metric)
            messages.append(perf_message)
        
        # Earnings calendar message
        if earnings_data:
            earnings_message = self.format_earnings_message(earnings_data)
            messages.append(earnings_message)
        
        # Send all messages
        success = True
        for message in messages:
            if len(message) > 4096:  # Telegram message limit
                # Split long messages
                chunks = self._split_message(message, 4096)
                for chunk in chunks:
                    success &= self.send_message(chunk)
            else:
                success &= self.send_message(message)
        
        return success
    
    def _split_message(self, message: str, max_length: int) -> List[str]:
        """Split long messages into chunks"""
        chunks = []
        lines = message.split('\n')
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk + line + '\n') <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def send_alert(self, message: str, urgent: bool = False) -> bool:
        """Send an alert message"""
        alert_prefix = "[URGENT]" if urgent else "[INFO]"
        formatted_message = f"{alert_prefix} <b>MARKET ALERT</b>\n\n{message}"
        return self.send_message(formatted_message)
    
    def test_connection(self) -> bool:
        """Test if the bot can send messages"""
        current_time = datetime.now()
        test_message = "Bot connection test successful!\n" + \
                      f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n" + \
                      f"Timestamp: {current_time.isoformat()}"
        
        return self.send_message(test_message)

# Configuration helper
class TelegramConfig:
    """Helper class to manage Telegram configuration"""
    
    @staticmethod
    def save_config(bot_token: str, chat_id: str, filename: str = "telegram_config.json"):
        """Save Telegram configuration to file"""
        config = {
            'bot_token': bot_token,
            'chat_id': chat_id,
            'created': datetime.now().isoformat()
        }
        
        filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Telegram config saved to: {filepath}")
        return filepath
    
    @staticmethod
    def load_config(filename: str = "telegram_config.json") -> Dict:
        """Load Telegram configuration from file"""
        try:
            filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
            with open(filepath, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Error loading Telegram config: {e}")
            return {}

def main():
    """Main function to demonstrate the Telegram bot"""
    # You need to set these values:
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
    CHAT_ID = "YOUR_CHAT_ID_HERE"      # Your chat ID or channel ID
    
    # Create bot instance
    bot = TelegramBot(BOT_TOKEN, CHAT_ID)
    
    # Test connection
    print("Testing Telegram bot connection...")
    if bot.test_connection():
        print("Bot is working!")
    else:
        print("Bot test failed. Check your token and chat ID.")
        return
    
    # Example: Send sample market update
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
    bot.send_market_update(
        top_performers=sample_performers,
        earnings_data=sample_earnings,
        metric='return_pct'
    )

if __name__ == "__main__":
    main()