#!/usr/bin/env python3
"""
Unified Market Analysis System
Runs both real-time news monitoring and comprehensive market analysis in parallel
"""

import sys
import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
from flash_news_monitor import FlashNewsMonitor
from sp500_tracker import SP500Tracker
from earnings_calendar import EarningsCalendar
from telegram_bot import TelegramBot
from sentiment_analyzer import SentimentAnalyzer
from config_loader import load_config

class UnifiedMarketSystem:
    def __init__(self):
        """Initialize the unified market analysis system"""
        print("🚀 UNIFIED MARKET ANALYSIS SYSTEM")
        print("=" * 50)
        
        # Load configuration
        self.config = load_config()
        if not self.config:
            raise Exception("Could not load configuration")
        
        # Extract Telegram settings
        self.bot_token = self.config['telegram']['bot_token']
        self.chat_id = self.config['telegram']['chat_id']
        
        # Initialize components
        self._initialize_components()
        
        # Threading control
        self.running = False
        self.news_monitor_thread = None
        self.market_analysis_thread = None
        
        # Analysis settings from config
        self.analysis_settings = self.config['monitoring']
        
    def _initialize_components(self):
        """Initialize all system components"""
        print("Initializing system components...")
        
        # 1. Flash News Monitor
        self.news_monitor = FlashNewsMonitor(
            bot_token=self.bot_token,
            chat_id=self.chat_id,
            news_api_key=self.config['news_apis'].get('news_api_key')
        )
        
        # Set monitored symbols from config
        symbols = self.config['monitoring']['symbols_to_monitor']
        self.news_monitor.monitored_symbols = set(symbols)
        
        # 2. Market Analysis Components
        self.sp500_tracker = SP500Tracker()
        self.earnings_calendar = EarningsCalendar(
            alpha_vantage_key=self.config['news_apis'].get('alpha_vantage_key')
        )
        self.sentiment_analyzer = SentimentAnalyzer(
            news_api_key=self.config['news_apis'].get('news_api_key')
        )
        
        # 3. Enhanced Telegram Bot
        self.telegram_bot = TelegramBot(
            self.bot_token,
            self.chat_id
        )
        
        print("✅ All components initialized successfully")
    
    def start_unified_system(self):
        """Start both systems in parallel"""
        if self.running:
            print("System is already running!")
            return
        
        print("\n🌟 Starting Unified Market Analysis System...")
        print("=" * 50)
        
        self.running = True
        
        # Start real-time news monitoring in background
        print("📰 Starting real-time news monitoring...")
        self.news_monitor_thread = threading.Thread(
            target=self._run_news_monitoring,
            daemon=True
        )
        self.news_monitor_thread.start()
        
        # Start comprehensive market analysis in background
        print("📊 Starting comprehensive market analysis...")
        self.market_analysis_thread = threading.Thread(
            target=self._run_market_analysis,
            daemon=True
        )
        self.market_analysis_thread.start()
        
        # Send startup notification
        if self.config['monitoring'].get('send_startup_notification', True):
            self._send_startup_notification()
        
        print("\n✅ UNIFIED SYSTEM ACTIVE")
        print("=" * 30)
        print("📰 Real-time news alerts: RUNNING")
        print("📊 Market analysis reports: RUNNING")
        print("⏰ Press Ctrl+C to stop all systems")
        print("=" * 30)
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_unified_system()
    
    def _run_news_monitoring(self):
        """Run the news monitoring system"""
        try:
            interval_minutes = self.config['monitoring']['check_interval_minutes']
            print(f"📰 News monitoring: Checking every {interval_minutes} minutes")
            
            while self.running:
                try:
                    # Get and process news alerts
                    alerts = self.news_monitor.get_all_news()
                    
                    # Send high-priority alerts immediately
                    for alert in alerts:
                        if alert.urgency_score >= self.config['monitoring'].get('minimum_urgency_score', 3):
                            formatted_message = self.news_monitor.format_alert_message(alert)
                            success = self.telegram_bot.send_message(formatted_message)
                            
                            if success:
                                print(f"📨 Sent news alert: {alert.title[:50]}...")
                            else:
                                print(f"❌ Failed to send alert: {alert.title[:50]}...")
                    
                    # Wait for next check
                    for _ in range(interval_minutes * 60):  # Convert to seconds
                        if not self.running:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"❌ News monitoring error: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
                    
        except Exception as e:
            print(f"❌ Critical news monitoring error: {e}")
    
    def _run_market_analysis(self):
        """Run comprehensive market analysis"""
        try:
            # Initial analysis
            time.sleep(30)  # Give news monitoring time to start
            
            while self.running:
                try:
                    print("\n📊 Running comprehensive market analysis...")
                    
                    # Run full market analysis
                    results = self._perform_market_analysis()
                    
                    # Send comprehensive report
                    if results and not results.get('errors'):
                        self._send_market_report(results)
                        print("✅ Market analysis report sent")
                    else:
                        print("⚠️ Market analysis completed with issues")
                    
                    # Wait for next analysis (4 hours = 14400 seconds)
                    analysis_interval = 4 * 60 * 60  # 4 hours
                    print(f"⏰ Next market analysis in 4 hours...")
                    
                    for _ in range(analysis_interval):
                        if not self.running:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"❌ Market analysis error: {e}")
                    time.sleep(3600)  # Wait 1 hour before retrying
                    
        except Exception as e:
            print(f"❌ Critical market analysis error: {e}")
    
    def _perform_market_analysis(self):
        """Perform comprehensive market analysis"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'top_performers': [],
            'earnings_calendar': [],
            'sentiment_analysis': [],
            'errors': []
        }
        
        try:
            # Step 1: Get top performers
            print("📈 Analyzing S&P 500 top performers...")
            top_performers_df = self.sp500_tracker.get_top_performers(
                metric='return_pct',
                top_n=15,
                period='1mo'
            )
            
            if not top_performers_df.empty:
                results['top_performers'] = top_performers_df.to_dict('records')
                print(f"✅ Found {len(results['top_performers'])} top performers")
            
            # Step 2: Get earnings calendar
            if results['top_performers']:
                print("📅 Checking earnings calendar...")
                symbols = [company['symbol'] for company in results['top_performers'][:25]]
                
                earnings_info = self.earnings_calendar.get_company_earnings_info(symbols)
                upcoming_earnings = self.earnings_calendar.filter_upcoming_earnings(
                    earnings_info, days_ahead=30
                )
                
                results['earnings_calendar'] = upcoming_earnings
                print(f"✅ Found {len(upcoming_earnings)} upcoming earnings")
            
            # Step 3: Sentiment analysis (optional - only if NewsAPI available)
            if self.config['news_apis'].get('news_api_key') and results['top_performers']:
                print("🎯 Performing sentiment analysis...")
                top_companies = results['top_performers'][:10]  # Limit to top 10
                
                sentiment_results = self.sentiment_analyzer.analyze_multiple_companies(top_companies)
                results['sentiment_analysis'] = sentiment_results
                print(f"✅ Analyzed sentiment for {len(sentiment_results)} companies")
            
        except Exception as e:
            error_msg = f"Market analysis error: {e}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        return results
    
    def _send_startup_notification(self):
        """Send system startup notification"""
        startup_message = f"""
🚀 <b>UNIFIED MARKET SYSTEM STARTED</b>

<b>System Status:</b> ACTIVE
<b>Started:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>Active Components:</b>
📰 Real-time news monitoring ({self.config['monitoring']['check_interval_minutes']} min intervals)
📊 Market analysis reports (4 hour intervals)
📅 Earnings calendar tracking
🎯 Sentiment analysis (when available)

<b>Monitoring {len(self.config['monitoring']['symbols_to_monitor'])} symbols:</b>
{', '.join(self.config['monitoring']['symbols_to_monitor'][:10])}...

<b>Alert Settings:</b>
• Minimum urgency: {self.config['monitoring'].get('minimum_urgency_score', 3)}/10
• Max alerts per hour: {self.config['monitoring'].get('max_alerts_per_hour', 10)}

System ready for market monitoring! 📈
"""
        
        self.telegram_bot.send_message(startup_message.strip())
    
    def _send_market_report(self, results):
        """Send comprehensive market analysis report"""
        try:
            # Send top performers report
            if results['top_performers']:
                performers_message = self.telegram_bot.format_top_performers_message(
                    results['top_performers'], 
                    'return_pct'
                )
                self.telegram_bot.send_message(performers_message)
            
            # Send earnings calendar report
            if results['earnings_calendar']:
                earnings_message = self.telegram_bot.format_earnings_message(
                    results['earnings_calendar']
                )
                self.telegram_bot.send_message(earnings_message)
            
            # Send sentiment summary if available
            if results['sentiment_analysis']:
                sentiment_summary = self._format_sentiment_summary(results['sentiment_analysis'])
                self.telegram_bot.send_message(sentiment_summary)
                
        except Exception as e:
            print(f"❌ Error sending market report: {e}")
    
    def _format_sentiment_summary(self, sentiment_data):
        """Format sentiment analysis summary"""
        if not sentiment_data:
            return ""
        
        positive_count = sum(1 for item in sentiment_data if item.get('overall_sentiment', 'neutral') == 'positive')
        negative_count = sum(1 for item in sentiment_data if item.get('overall_sentiment', 'neutral') == 'negative')
        neutral_count = len(sentiment_data) - positive_count - negative_count
        
        message = f"""
📊 <b>SENTIMENT ANALYSIS SUMMARY</b>

<b>Overall Market Sentiment:</b>
✅ Positive: {positive_count} stocks
❌ Negative: {negative_count} stocks  
➖ Neutral: {neutral_count} stocks

<b>Analysis Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<b>Companies Analyzed:</b> {len(sentiment_data)}

<i>Detailed sentiment data saved locally</i>
"""
        return message.strip()
    
    def stop_unified_system(self):
        """Stop all systems gracefully"""
        print("\n🛑 Stopping Unified Market System...")
        
        self.running = False
        
        # Stop news monitoring
        if hasattr(self.news_monitor, 'stop_monitoring'):
            self.news_monitor.stop_monitoring()
        
        # Wait for threads to finish
        if self.news_monitor_thread and self.news_monitor_thread.is_alive():
            self.news_monitor_thread.join(timeout=5)
        
        if self.market_analysis_thread and self.market_analysis_thread.is_alive():
            self.market_analysis_thread.join(timeout=5)
        
        # Send shutdown notification
        shutdown_message = f"""
🛑 <b>UNIFIED MARKET SYSTEM STOPPED</b>

<b>Shutdown Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<b>Status:</b> All monitoring systems offline

System shutdown complete. 📴
"""
        
        try:
            self.telegram_bot.send_message(shutdown_message.strip())
        except:
            pass
        
        print("✅ All systems stopped successfully")

def main():
    """Main entry point"""
    try:
        system = UnifiedMarketSystem()
        system.start_unified_system()
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user")
    except Exception as e:
        print(f"❌ Critical system error: {e}")
    finally:
        print("Unified Market System terminated.")

if __name__ == "__main__":
    main()