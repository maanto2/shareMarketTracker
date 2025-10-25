"""
Market Analysis Orchestrator
Main script that combines all modules and runs the complete workflow
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
from sp500_tracker import SP500Tracker
from earnings_calendar import EarningsCalendar
from telegram_bot import TelegramBot, TelegramConfig
from sentiment_analyzer import SentimentAnalyzer

class MarketAnalysisOrchestrator:
    def __init__(self, config_file: str = "market_config.json"):
        """Initialize the market analysis orchestrator"""
        self.config = self._load_config(config_file)
        
        # Initialize modules
        self.sp500_tracker = SP500Tracker()
        self.earnings_calendar = EarningsCalendar(
            alpha_vantage_key=self.config.get('alpha_vantage_key')
        )
        self.sentiment_analyzer = SentimentAnalyzer(
            news_api_key=self.config.get('news_api_key')
        )
        
        # Initialize Telegram bot if configured
        self.telegram_bot = None
        if self.config.get('telegram_bot_token') and self.config.get('telegram_chat_id'):
            self.telegram_bot = TelegramBot(
                self.config['telegram_bot_token'],
                self.config['telegram_chat_id']
            )
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        try:
            filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{config_file}"
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using default settings.")
            return self._create_default_config(config_file)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def _create_default_config(self, config_file: str) -> Dict:
        """Create default configuration file"""
        default_config = {
            "alpha_vantage_key": None,
            "news_api_key": None,
            "telegram_bot_token": None,
            "telegram_chat_id": None,
            "analysis_settings": {
                "top_performers_count": 25,
                "performance_period": "1mo",
                "earnings_days_ahead": 30,
                "sentiment_days_back": 7,
                "min_market_cap": 1000000000
            },
            "schedule": {
                "daily_update_time": "09:00",
                "weekly_summary_day": "monday",
                "earnings_alert_days": [1, 3, 7]
            }
        }
        
        try:
            filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{config_file}"
            with open(filepath, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config file: {filepath}")
        except Exception as e:
            print(f"Error creating config file: {e}")
        
        return default_config
    
    def run_full_analysis(self, 
                         metric: str = 'return_pct',
                         send_telegram: bool = True) -> Dict:
        """Run complete market analysis workflow"""
        
        print("Starting Market Analysis Workflow")
        print("=" * 50)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric,
            'top_performers': [],
            'earnings_calendar': [],
            'sentiment_analysis': [],
            'errors': []
        }
        
        # Step 1: Get top performers
        try:
            print("\nStep 1: Getting top S&P 500 performers...")
            settings = self.config.get('analysis_settings', {})
            
            top_performers_df = self.sp500_tracker.get_top_performers(
                metric=metric,
                top_n=settings.get('top_performers_count', 15),
                period=settings.get('performance_period', '1mo'),
                min_market_cap=settings.get('min_market_cap', 1000000000)
            )
            
            if not top_performers_df.empty:
                results['top_performers'] = top_performers_df.to_dict('records')
                
                # Save top performers
                self.sp500_tracker.save_top_performers(top_performers_df, metric=metric)
                
                # Print summary
                summary = self.sp500_tracker.get_performance_summary(top_performers_df, metric)
                print(summary)
            else:
                print("❌ No top performers data available")
                results['errors'].append("No top performers data available")
                
        except Exception as e:
            error_msg = f"Error in top performers analysis: {e}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
        
        # Step 2: Get earnings calendar for top performers
        try:
            print("\nStep 2: Getting earnings calendar...")
            if results['top_performers']:
                # Get symbols from top performers
                symbols = [company['symbol'] for company in results['top_performers'][:25]]
                
                earnings_info = self.earnings_calendar.get_company_earnings_info(symbols)
                
                # Filter for upcoming earnings
                settings = self.config.get('analysis_settings', {})
                upcoming_earnings = self.earnings_calendar.filter_upcoming_earnings(
                    earnings_info, 
                    days_ahead=settings.get('earnings_days_ahead', 30)
                )
                
                results['earnings_calendar'] = upcoming_earnings
                
                # Save earnings calendar
                if earnings_info:
                    self.earnings_calendar.save_earnings_calendar(earnings_info)
                
                # Print summary
                if upcoming_earnings:
                    summary = self.earnings_calendar.generate_earnings_summary(upcoming_earnings)
                    print(summary)
                else:
                    print("No upcoming earnings found for top performers")
            else:
                print("⚠️ Skipping earnings calendar (no top performers)")
                
        except Exception as e:
            error_msg = f"Error in earnings calendar analysis: {e}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
        
        # Step 3: Sentiment analysis
        try:
            print("\nStep 3: Performing sentiment analysis...")
            if results['top_performers']:
                # Get top 25 for sentiment analysis
                top_companies = results['top_performers'][:25]
                
                sentiment_results = self.sentiment_analyzer.analyze_multiple_companies(top_companies)
                results['sentiment_analysis'] = sentiment_results
                
                # Save sentiment analysis
                self.sentiment_analyzer.save_sentiment_analysis(sentiment_results)
                
                # Print summary
                summary = self.sentiment_analyzer.get_sentiment_summary(sentiment_results)
                print(summary)
            else:
                print("⚠️ Skipping sentiment analysis (no top performers)")
                
        except Exception as e:
            error_msg = f"Error in sentiment analysis: {e}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
        
        # Step 4: Send Telegram notifications
        if send_telegram and self.telegram_bot:
            try:
                print("\nStep 4: Sending Telegram notifications...")
                
                success = self.telegram_bot.send_market_update(
                    top_performers=results['top_performers'],
                    earnings_data=results['earnings_calendar'],
                    sentiment_data=results.get('sentiment_analysis', []),
                    metric=metric
                )
                
                if success:
                    print("✅ Telegram notifications sent successfully")
                else:
                    print("❌ Failed to send Telegram notifications")
                    results['errors'].append("Failed to send Telegram notifications")
                    
            except Exception as e:
                error_msg = f"Error sending Telegram notifications: {e}"
                print(f"❌ {error_msg}")
                results['errors'].append(error_msg)
        elif send_telegram:
            print("⚠️ Telegram not configured - skipping notifications")
        else:
            print("⚠️ Telegram notifications disabled")
        
        # Save complete results
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_analysis_complete_{timestamp}.json"
            filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
            
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"\nComplete results saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
        
        print("\nMarket Analysis Workflow Completed!")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Top performers found: {len(results['top_performers'])}")
        print(f"Upcoming earnings: {len(results['earnings_calendar'])}")
        print(f"Sentiment analyzed: {len(results['sentiment_analysis'])}")
        print(f"Errors encountered: {len(results['errors'])}")
        
        return results
    
    def run_quick_analysis(self, symbols: List[str]) -> Dict:
        """Run quick analysis for specific symbols"""
        print(f"Running quick analysis for: {', '.join(symbols)}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'symbols': symbols,
            'performance_data': [],
            'earnings_data': [],
            'sentiment_data': []
        }
        
        # Get performance data
        for symbol in symbols:
            perf_data = self.sp500_tracker.get_stock_performance(symbol)
            if perf_data:
                results['performance_data'].append(perf_data)
        
        # Get earnings data
        earnings_data = self.earnings_calendar.get_company_earnings_info(symbols)
        results['earnings_data'] = earnings_data
        
        # Get sentiment data
        companies = [{'symbol': s} for s in symbols]
        sentiment_data = self.sentiment_analyzer.analyze_multiple_companies(companies)
        results['sentiment_data'] = sentiment_data
        
        return results
    
    def setup_configuration(self):
        """Interactive setup for configuration"""
        print("🔧 Market Analysis Configuration Setup")
        print("=" * 40)
        
        config = {}
        
        # API Keys
        print("\nAPI Keys (optional but recommended):")
        config['alpha_vantage_key'] = input("Alpha Vantage API Key (press Enter to skip): ").strip() or None
        config['news_api_key'] = input("News API Key (press Enter to skip): ").strip() or None
        
        # Telegram Configuration
        print("\nTelegram Bot Setup:")
        bot_token = input("Telegram Bot Token (from @BotFather): ").strip()
        chat_id = input("Telegram Chat ID: ").strip()
        
        if bot_token and chat_id:
            config['telegram_bot_token'] = bot_token
            config['telegram_chat_id'] = chat_id
            
            # Test Telegram connection
            print("Testing Telegram connection...")
            test_bot = TelegramBot(bot_token, chat_id)
            if test_bot.test_connection():
                print("✅ Telegram connection successful!")
            else:
                print("❌ Telegram connection failed. Please check your credentials.")
        
        # Analysis Settings
        print("\nAnalysis Settings:")
        config['analysis_settings'] = {
            'top_performers_count': int(input("Number of top performers to analyze (default 25): ") or 25),
            'performance_period': input("Performance period (1mo/3mo/6mo, default 1mo): ") or "1mo",
            'earnings_days_ahead': int(input("Days ahead for earnings calendar (default 30): ") or 30),
            'sentiment_days_back': int(input("Days back for sentiment analysis (default 7): ") or 7),
            'min_market_cap': int(input("Minimum market cap in billions (default 1): ") or 1) * 1000000000
        }
        
        # Save configuration
        config_file = "market_config.json"
        filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{config_file}"
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✅ Configuration saved to: {filepath}")
        return config

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Market Analysis Tool')
    parser.add_argument('--setup', action='store_true', help='Run configuration setup')
    parser.add_argument('--metric', default='return_pct', choices=['return_pct', 'volume_ratio', 'volatility'], help='Performance metric to analyze')
    parser.add_argument('--no-telegram', action='store_true', help='Skip Telegram notifications')
    parser.add_argument('--quick', nargs='+', help='Quick analysis for specific symbols')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = MarketAnalysisOrchestrator()
    
    # Run setup if requested
    if args.setup:
        orchestrator.setup_configuration()
        return
    
    # Run quick analysis if requested
    if args.quick:
        results = orchestrator.run_quick_analysis(args.quick)
        print(json.dumps(results, indent=2, default=str))
        return
    
    # Run full analysis
    results = orchestrator.run_full_analysis(
        metric=args.metric,
        send_telegram=not args.no_telegram
    )

if __name__ == "__main__":
    main()