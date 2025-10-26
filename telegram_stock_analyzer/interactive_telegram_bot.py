#!/usr/bin/env python3
"""
Interactive Telegram Bot for Stock Analysis
Responds to user messages with stock analysis and BUY/SELL recommendations
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import threading
from stock_analyzer import StockAnalyzer
from prediction_engine import PredictionEngine

class InteractiveTelegramBot:
    def __init__(self, bot_token: str, authorized_chat_ids: List[str] = None):
        """
        Initialize interactive Telegram bot
        
        Args:
            bot_token: Your Telegram bot token from @BotFather
            authorized_chat_ids: List of chat IDs authorized to use the bot
        """
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.authorized_chat_ids = set(authorized_chat_ids) if authorized_chat_ids else set()
        
        # Initialize components
        self.stock_analyzer = StockAnalyzer()
        self.prediction_engine = PredictionEngine()
        
        # Bot state
        self.running = False
        self.last_update_id = 0
        
        print("🤖 Interactive Telegram Stock Bot initialized")
        print(f"📱 Authorized users: {len(self.authorized_chat_ids)}")
    
    def send_message(self, chat_id: str, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to specific chat"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            
            if result['ok']:
                return True
            else:
                print(f"❌ Error sending message: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Exception sending message: {e}")
            return False
    
    def get_updates(self, offset: int = None, timeout: int = 30) -> List[Dict]:
        """Get updates from Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                'timeout': timeout,
                'allowed_updates': ['message']
            }
            
            if offset:
                params['offset'] = offset
            
            response = requests.get(url, params=params, timeout=35)
            result = response.json()
            
            if result['ok']:
                return result['result']
            else:
                print(f"❌ Error getting updates: {result}")
                return []
                
        except Exception as e:
            print(f"❌ Exception getting updates: {e}")
            return []
    
    def is_authorized(self, chat_id: str) -> bool:
        """Check if chat_id is authorized to use the bot"""
        if not self.authorized_chat_ids:
            return True  # If no restrictions, allow all
        return str(chat_id) in self.authorized_chat_ids
    
    def process_stock_command(self, chat_id: str, symbol: str) -> str:
        """Process stock analysis command"""
        try:
            print(f"📊 Analyzing stock: {symbol} for chat {chat_id}")
            
            # Send "typing" action to show bot is working
            self.send_typing_action(chat_id)
            
            # Get stock analysis
            analysis = self.stock_analyzer.analyze_stock(symbol)
            
            if not analysis or analysis.get('error'):
                error_msg = analysis.get('error', 'Unknown error') if analysis else 'Failed to analyze stock'
                return f"❌ <b>Error analyzing {symbol.upper()}</b>\n\n{error_msg}\n\nPlease check the symbol and try again."
            
            # Get prediction
            prediction = self.prediction_engine.get_prediction(analysis)
            
            # Format response message
            message = self.format_stock_analysis_message(analysis, prediction)
            
            return message
            
        except Exception as e:
            print(f"❌ Error processing stock command for {symbol}: {e}")
            return f"❌ <b>Error</b>\n\nFailed to analyze {symbol.upper()}. Please try again later.\n\nError: {str(e)}"
    
    def send_typing_action(self, chat_id: str):
        """Send typing action to show bot is working"""
        try:
            url = f"{self.base_url}/sendChatAction"
            data = {
                'chat_id': chat_id,
                'action': 'typing'
            }
            requests.post(url, data=data, timeout=5)
        except:
            pass  # Non-critical action
    
    def format_stock_analysis_message(self, analysis: Dict, prediction: Dict) -> str:
        """Format stock analysis into readable message"""
        symbol = analysis.get('symbol', 'N/A').upper()
        company_name = analysis.get('company_name', 'Unknown Company')
        current_price = analysis.get('current_price', 0)
        
        # Header
        message = f"📊 <b>STOCK ANALYSIS: {symbol}</b>\n"
        message += f"<i>{company_name}</i>\n"
        message += f"💰 Current Price: <b>${current_price:.2f}</b>\n\n"
        
        # Trading Recommendation (Most Important)
        rec = prediction.get('recommendation', {})
        action = rec.get('action', 'HOLD')
        confidence = rec.get('confidence', 0)
        reason = rec.get('reason', 'No specific reason provided')
        
        # Action emoji and formatting
        if action == 'BUY':
            if confidence >= 80:
                action_emoji = "🟢🟢"
                action_text = f"<b>STRONG BUY</b>"
            elif confidence >= 60:
                action_emoji = "🟢"
                action_text = f"<b>BUY</b>"
            else:
                action_emoji = "🟡"
                action_text = f"<b>WEAK BUY</b>"
        elif action == 'SELL':
            if confidence >= 80:
                action_emoji = "🔴🔴"
                action_text = f"<b>STRONG SELL</b>"
            elif confidence >= 60:
                action_emoji = "🔴"
                action_text = f"<b>SELL</b>"
            else:
                action_emoji = "🟠"
                action_text = f"<b>WEAK SELL</b>"
        else:
            action_emoji = "⚪"
            action_text = f"<b>HOLD</b>"
        
        message += f"🎯 <b>RECOMMENDATION</b>\n"
        message += f"{action_emoji} {action_text}\n"
        message += f"📈 Confidence: <b>{confidence:.1f}%</b>\n"
        message += f"💡 Reason: {reason}\n\n"
        
        # Technical Analysis
        technical = analysis.get('technical_analysis', {})
        if technical:
            message += f"📈 <b>TECHNICAL ANALYSIS</b>\n"
            
            # Price performance
            day_change = technical.get('day_change_pct', 0)
            week_change = technical.get('week_change_pct', 0)
            month_change = technical.get('month_change_pct', 0)
            
            day_emoji = "🟢" if day_change > 0 else "🔴" if day_change < 0 else "⚪"
            week_emoji = "🟢" if week_change > 0 else "🔴" if week_change < 0 else "⚪"
            month_emoji = "🟢" if month_change > 0 else "🔴" if month_change < 0 else "⚪"
            
            message += f"{day_emoji} 1-Day: <b>{day_change:+.2f}%</b>\n"
            message += f"{week_emoji} 1-Week: <b>{week_change:+.2f}%</b>\n"
            message += f"{month_emoji} 1-Month: <b>{month_change:+.2f}%</b>\n"
            
            # Volume analysis
            volume_ratio = technical.get('volume_ratio', 0)
            volume_emoji = "📈" if volume_ratio > 1.5 else "📊" if volume_ratio > 0.8 else "📉"
            message += f"{volume_emoji} Volume Ratio: <b>{volume_ratio:.2f}x</b>\n"
            
            # RSI
            rsi = technical.get('rsi', 0)
            if rsi > 70:
                rsi_status = "🔴 Overbought"
            elif rsi < 30:
                rsi_status = "🟢 Oversold"
            else:
                rsi_status = "⚪ Neutral"
            message += f"📊 RSI: <b>{rsi:.1f}</b> {rsi_status}\n\n"
        
        # Sentiment Analysis
        sentiment = analysis.get('sentiment_analysis', {})
        if sentiment:
            overall_sentiment = sentiment.get('overall_sentiment', 'neutral')
            sentiment_score = sentiment.get('overall_score', 0)
            news_count = sentiment.get('articles_analyzed', 0)
            
            sentiment_emoji = "😊" if overall_sentiment == 'positive' else "😞" if overall_sentiment == 'negative' else "😐"
            
            message += f"📰 <b>NEWS SENTIMENT</b>\n"
            message += f"{sentiment_emoji} Overall: <b>{overall_sentiment.upper()}</b>\n"
            message += f"📊 Score: <b>{sentiment_score:+.2f}</b>\n"
            message += f"📄 Articles: <b>{news_count}</b>\n\n"
        
        # Market Data
        market_data = analysis.get('market_data', {})
        if market_data:
            market_cap = market_data.get('market_cap', 0)
            sector = market_data.get('sector', 'Unknown')
            pe_ratio = market_data.get('pe_ratio', 0)
            
            message += f"🏢 <b>COMPANY INFO</b>\n"
            message += f"🏭 Sector: <b>{sector}</b>\n"
            
            if market_cap > 0:
                if market_cap > 1e12:
                    cap_str = f"${market_cap/1e12:.2f}T"
                elif market_cap > 1e9:
                    cap_str = f"${market_cap/1e9:.2f}B"
                else:
                    cap_str = f"${market_cap/1e6:.2f}M"
                message += f"💰 Market Cap: <b>{cap_str}</b>\n"
            
            if pe_ratio > 0:
                message += f"📊 P/E Ratio: <b>{pe_ratio:.2f}</b>\n"
        
        # Footer with links
        message += f"\n🔗 <b>LINKS</b>\n"
        message += f"📈 <a href='https://finance.yahoo.com/quote/{symbol}'>Yahoo Finance</a>\n"
        message += f"📊 <a href='https://www.tradingview.com/symbols/{symbol}'>TradingView</a>\n"
        message += f"📰 <a href='https://finance.yahoo.com/quote/{symbol}/news'>Latest News</a>\n\n"
        
        # Disclaimer
        message += f"<i>⚠️ This is not financial advice. Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
        
        return message
    
    def process_help_command(self, chat_id: str) -> str:
        """Generate help message"""
        message = """📱 <b>STOCK ANALYZER BOT</b>

<b>🎯 COMMANDS:</b>
• Send any stock symbol (e.g., <code>AAPL</code>, <code>TSLA</code>, <code>MSFT</code>)
• <code>/help</code> - Show this help message
• <code>/status</code> - Check bot status

<b>📊 WHAT I ANALYZE:</b>
• 📈 Technical indicators (RSI, price trends, volume)
• 📰 News sentiment analysis
• 💰 Market data (P/E, market cap, sector)
• ⚖️ BUY/SELL/HOLD recommendations

<b>📝 EXAMPLES:</b>
• <code>AAPL</code> - Analyze Apple stock
• <code>TSLA</code> - Analyze Tesla stock
• <code>SPY</code> - Analyze S&P 500 ETF

<b>⚠️ DISCLAIMER:</b>
This is not financial advice. Always do your own research before making investment decisions.

Bot ready! 🚀"""
        
        return message
    
    def process_status_command(self, chat_id: str) -> str:
        """Generate status message"""
        current_time = datetime.now()
        
        message = f"""🤖 <b>BOT STATUS</b>

✅ <b>Status:</b> Online and Ready
⏰ <b>Current Time:</b> {current_time.strftime('%Y-%m-%d %H:%M:%S')}
🔄 <b>Last Update:</b> {current_time.strftime('%H:%M:%S')}

<b>🔧 CAPABILITIES:</b>
• ✅ Stock price analysis
• ✅ Technical indicators
• ✅ News sentiment analysis
• ✅ BUY/SELL predictions

<b>📊 READY TO ANALYZE STOCKS!</b>
Send me any stock symbol to get started."""
        
        return message
    
    def handle_message(self, update: Dict):
        """Handle incoming message"""
        try:
            message = update.get('message', {})
            chat_id = str(message.get('chat', {}).get('id', ''))
            text = message.get('text', '').strip()
            username = message.get('from', {}).get('username', 'Unknown')
            
            if not chat_id:
                return
            
            # Check authorization
            if not self.is_authorized(chat_id):
                self.send_message(chat_id, "❌ <b>Unauthorized</b>\n\nThis bot is restricted to authorized users only.")
                print(f"🚫 Unauthorized access attempt from {username} ({chat_id})")
                return
            
            print(f"📨 Message from {username} ({chat_id}): {text}")
            
            # Process commands
            if text.startswith('/help'):
                response = self.process_help_command(chat_id)
            elif text.startswith('/status'):
                response = self.process_status_command(chat_id)
            elif text.startswith('/'):
                response = "❓ Unknown command. Send /help for available commands."
            else:
                # Assume it's a stock symbol
                symbol = text.upper().strip()
                
                # Basic validation
                if len(symbol) < 1 or len(symbol) > 10:
                    response = "❌ <b>Invalid Symbol</b>\n\nPlease send a valid stock symbol (1-10 characters).\n\nExamples: AAPL, TSLA, MSFT"
                else:
                    response = self.process_stock_command(chat_id, symbol)
            
            # Send response
            success = self.send_message(chat_id, response)
            if success:
                print(f"✅ Response sent to {username}")
            else:
                print(f"❌ Failed to send response to {username}")
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
    
    def start_bot(self):
        """Start the bot polling loop"""
        print("🚀 Starting Interactive Telegram Stock Bot...")
        print("📡 Polling for messages...")
        
        self.running = True
        
        while self.running:
            try:
                # Get updates
                updates = self.get_updates(offset=self.last_update_id + 1)
                
                # Process each update
                for update in updates:
                    try:
                        self.handle_message(update)
                        self.last_update_id = update['update_id']
                    except Exception as e:
                        print(f"❌ Error processing update: {e}")
                
                # Small delay to prevent excessive API calls
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Shutting down bot...")
                self.running = False
            except Exception as e:
                print(f"❌ Polling error: {e}")
                print("⏸️ Waiting 5 seconds before retry...")
                time.sleep(5)
        
        print("✅ Bot stopped")
    
    def stop_bot(self):
        """Stop the bot"""
        self.running = False

def main():
    """Main function for testing"""
    # Configuration - Replace with your actual values
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
    AUTHORIZED_CHAT_IDS = ["YOUR_CHAT_ID_HERE"]  # Your Telegram chat ID
    
    # Create and start bot
    bot = InteractiveTelegramBot(BOT_TOKEN, AUTHORIZED_CHAT_IDS)
    
    try:
        bot.start_bot()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    main()