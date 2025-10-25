"""
Flash News Monitor for Stock Market
Monitors breaking news and sends Telegram alerts for market-moving events
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional
import re
from dataclasses import dataclass
import threading
import sys
import os
from config_loader import load_config

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot

@dataclass
class NewsAlert:
    """Represents a news alert"""
    title: str
    description: str
    url: str
    source: str
    published_at: str
    symbols_mentioned: List[str]
    urgency_score: int  # 1-10, 10 being most urgent
    keywords_matched: List[str]

class FlashNewsMonitor:
    def __init__(self, bot_token: str, chat_id: str, news_api_key: str = None):
        """
        Initialize the flash news monitor
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID
            news_api_key: Optional NewsAPI key for more comprehensive news
        """
        self.telegram_bot = TelegramBot(bot_token, chat_id)
        self.news_api_key = news_api_key
        
        # Stocks to monitor (can be customized)
        self.monitored_symbols = {
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 
            'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA', 'DIS',
            'NFLX', 'CRM', 'ADBE', 'PYPL', 'INTC', 'CSCO', 'PFE',
            'KO', 'PEP', 'WMT', 'BAC', 'XOM', 'CVX', 'T'
        }
        
        # High-impact keywords that trigger urgent alerts
        self.urgent_keywords = {
            'earnings beat', 'earnings miss', 'guidance raised', 'guidance lowered',
            'dividend increase', 'dividend cut', 'stock split', 'merger', 'acquisition',
            'partnership', 'breakthrough', 'fda approval', 'recall', 'lawsuit',
            'ceo', 'layoffs', 'hiring', 'bankruptcy', 'bailout', 'federal reserve',
            'interest rates', 'inflation', 'recession', 'market crash', 'correction',
            'all-time high', 'record low', 'halted trading', 'circuit breaker'
        }
        
        # Market impact keywords
        self.market_keywords = {
            'fed', 'federal reserve', 'jerome powell', 'interest rate', 'inflation',
            'unemployment', 'gdp', 'retail sales', 'consumer confidence',
            'oil prices', 'gold', 'bitcoin', 'cryptocurrency', 'nasdaq', 'dow jones',
            's&p 500', 'futures', 'premarket', 'after hours', 'volatility'
        }
        
        # Track sent alerts to avoid duplicates
        self.sent_alerts: Set[str] = set()
        
        # News sources for monitoring - Using general feeds to avoid rate limiting
        self.news_sources = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',  # General Yahoo Finance
            'https://feeds.marketwatch.com/marketwatch/realtimeheadlines/',  # MarketWatch
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',  # CNBC Markets
        ]
        
        self.running = False
        self.monitor_thread = None
        
    def add_monitored_symbols(self, symbols: List[str]):
        """Add symbols to monitoring list"""
        self.monitored_symbols.update(symbols)
        
    def remove_monitored_symbols(self, symbols: List[str]):
        """Remove symbols from monitoring list"""
        self.monitored_symbols.difference_update(symbols)
        
    def extract_symbols_from_text(self, text: str) -> List[str]:
        """Extract stock symbols mentioned in text"""
        symbols_found = []
        text_upper = text.upper()
        
        for symbol in self.monitored_symbols:
            # Look for symbol mentions
            patterns = [
                f' {symbol} ',  # Space separated
                f'({symbol})',  # In parentheses
                f'${symbol}',   # With dollar sign
                f'{symbol}:',   # With colon
                f'{symbol}.',   # With period
            ]
            
            for pattern in patterns:
                if pattern in text_upper:
                    symbols_found.append(symbol)
                    break
                    
        return list(set(symbols_found))  # Remove duplicates
        
    def calculate_urgency_score(self, title: str, description: str, symbols: List[str]) -> int:
        """Calculate urgency score (1-10) based on content"""
        score = 1
        text = (title + ' ' + description).lower()
        
        # High urgency keywords
        urgent_matches = sum(1 for keyword in self.urgent_keywords if keyword in text)
        score += min(urgent_matches * 2, 6)  # Max 6 points from urgent keywords
        
        # Market-wide impact
        market_matches = sum(1 for keyword in self.market_keywords if keyword in text)
        score += min(market_matches, 2)  # Max 2 points from market keywords
        
        # Multiple symbols mentioned
        if len(symbols) > 1:
            score += 1
            
        # Negative sentiment indicators
        negative_words = ['crash', 'plunge', 'collapse', 'emergency', 'crisis', 'halt']
        if any(word in text for word in negative_words):
            score += 2
            
        return min(score, 10)  # Cap at 10
        
    def get_news_from_rss(self, url: str) -> List[Dict]:
        """Get news from RSS feed"""
        try:
            # Add proper headers to avoid rate limiting
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                content = response.text
                
                # Basic RSS parsing
                articles = []
                
                # Extract items using regex (simple approach)
                items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
                
                for item in items:
                    # Try CDATA format first (Yahoo Finance)
                    title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
                    desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
                    
                    # If no CDATA, try regular format (MarketWatch, CNBC)
                    if not title_match:
                        title_match = re.search(r'<title>(.*?)</title>', item)
                    if not desc_match:
                        desc_match = re.search(r'<description>(.*?)</description>', item)
                    
                    link_match = re.search(r'<link>(.*?)</link>', item)
                    date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
                    
                    if title_match:
                        title = title_match.group(1).strip()
                        # Clean HTML entities
                        title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                        title = re.sub(r'&#x[0-9a-fA-F]+;', '', title)  # Remove hex entities
                        
                        description = desc_match.group(1).strip() if desc_match else ''
                        description = description.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                        
                        articles.append({
                            'title': title,
                            'description': description,
                            'url': link_match.group(1).strip() if link_match else url,
                            'published_at': date_match.group(1) if date_match else datetime.now().isoformat(),
                            'source': 'MarketWatch' if 'marketwatch' in url.lower() else 'CNBC' if 'cnbc' in url.lower() else 'Yahoo Finance'
                        })
                
                return articles[:10]  # Limit to 10 most recent
                
        except Exception as e:
            print(f"Error fetching RSS from {url}: {e}")
            
        return []
        
    def get_news_from_newsapi(self, query: str = "stock market") -> List[Dict]:
        """Get breaking news from NewsAPI"""
        if not self.news_api_key:
            return []
            
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 20,
                'from': (datetime.now() - timedelta(hours=1)).isoformat(),
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
                
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
            
        return []
        
    def get_all_news(self) -> List[NewsAlert]:
        """Get news from all sources and create alerts"""
        all_alerts = []
        
        # Get RSS feed news with rate limiting
        import time
        for i, rss_url in enumerate(self.news_sources):
            if i > 0:  # Add delay between requests to avoid rate limiting
                time.sleep(2)
            
            articles = self.get_news_from_rss(rss_url)
            for article in articles:
                symbols = self.extract_symbols_from_text(article['title'] + ' ' + article['description'])
                
                if symbols:  # Only create alert if relevant symbols found
                    urgency = self.calculate_urgency_score(
                        article['title'], 
                        article['description'], 
                        symbols
                    )
                    
                    # Clean up URL and source
                    news_url = article['url']
                    if not news_url.startswith('http'):
                        news_url = f"https://finance.yahoo.com{news_url}" if news_url.startswith('/') else news_url
                    
                    source_name = "Yahoo Finance" if "Yahoo Finance" in article['source'] else article['source']
                    
                    alert = NewsAlert(
                        title=article['title'],
                        description=article['description'],
                        url=news_url,
                        source=source_name,
                        published_at=article['published_at'],
                        symbols_mentioned=symbols,
                        urgency_score=urgency,
                        keywords_matched=self.find_matched_keywords(article['title'] + ' ' + article['description'])
                    )
                    all_alerts.append(alert)
        
        # Get NewsAPI news
        newsapi_articles = self.get_news_from_newsapi()
        for article in newsapi_articles:
            title = article.get('title', '')
            description = article.get('description', '')
            symbols = self.extract_symbols_from_text(title + ' ' + description)
            
            if symbols:
                urgency = self.calculate_urgency_score(title, description, symbols)
                
                alert = NewsAlert(
                    title=title,
                    description=description,
                    url=article.get('url', ''),
                    source=article.get('source', {}).get('name', 'NewsAPI'),
                    published_at=article.get('publishedAt', ''),
                    symbols_mentioned=symbols,
                    urgency_score=urgency,
                    keywords_matched=self.find_matched_keywords(title + ' ' + description)
                )
                all_alerts.append(alert)
        
        # Sort by urgency score (highest first)
        all_alerts.sort(key=lambda x: x.urgency_score, reverse=True)
        
        return all_alerts
        
    def find_matched_keywords(self, text: str) -> List[str]:
        """Find which keywords matched in the text"""
        text_lower = text.lower()
        matched = []
        
        for keyword in self.urgent_keywords.union(self.market_keywords):
            if keyword in text_lower:
                matched.append(keyword)
                
        return matched
        
    def format_alert_message(self, alert: NewsAlert) -> str:
        """Format alert for Telegram message"""
        urgency_emoji = ""
        if alert.urgency_score >= 8:
            urgency_emoji = "[URGENT] "
        elif alert.urgency_score >= 6:
            urgency_emoji = "[HIGH] "
        elif alert.urgency_score >= 4:
            urgency_emoji = "[MEDIUM] "
        else:
            urgency_emoji = "[LOW] "
            
        symbols_str = ", ".join(alert.symbols_mentioned)
        
        message = f"{urgency_emoji}<b>MARKET NEWS ALERT</b>\n\n"
        message += f"<b>Symbols:</b> {symbols_str}\n"
        message += f"<b>Urgency:</b> {alert.urgency_score}/10\n\n"
        message += f"<b>{alert.title}</b>\n\n"
        
        if alert.description and alert.description != alert.title:
            # Truncate description if too long
            desc = alert.description[:300] + "..." if len(alert.description) > 300 else alert.description
            message += f"{desc}\n\n"
        
        # Format timestamps - both published time and current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Try to parse published time
        published_time = "Unknown"
        if alert.published_at:
            try:
                if isinstance(alert.published_at, str):
                    # Handle different timestamp formats
                    if 'T' in alert.published_at:  # ISO format
                        pub_dt = datetime.fromisoformat(alert.published_at.replace('Z', '+00:00'))
                        published_time = pub_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                    else:  # RSS format
                        published_time = alert.published_at
                else:
                    published_time = str(alert.published_at)
            except:
                published_time = str(alert.published_at)
        
        message += f"<b>Source:</b> {alert.source}\n"
        message += f"<b>Published:</b> {published_time}\n"
        message += f"<b>Alert Time:</b> {current_time}\n"
        
        if alert.keywords_matched:
            keywords_str = ", ".join(alert.keywords_matched[:5])  # Show first 5 keywords
            message += f"<b>Keywords:</b> {keywords_str}\n"
        
        # Add clickable link with better formatting
        if alert.url and alert.url.strip():
            # Clean the URL
            clean_url = alert.url.strip()
            if not clean_url.startswith('http'):
                clean_url = 'https://' + clean_url
            message += f"\n📰 <a href='{clean_url}'>Read Full Article</a>"
        else:
            # If no URL, try to create a search link
            search_query = "+".join(alert.title.split()[:5])  # First 5 words
            search_url = f"https://www.google.com/search?q={search_query}+stock+news"
            message += f"\n🔍 <a href='{search_url}'>Search for More Info</a>"
            
        return message
        
    def should_send_alert(self, alert: NewsAlert) -> bool:
        """Determine if alert should be sent"""
        # Create unique identifier for this alert
        alert_id = f"{alert.title[:50]}_{','.join(sorted(alert.symbols_mentioned))}"
        
        # Skip if already sent
        if alert_id in self.sent_alerts:
            return False
            
        # Skip low urgency alerts unless they mention high-value stocks
        high_value_stocks = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA'}
        mentioned_high_value = any(symbol in high_value_stocks for symbol in alert.symbols_mentioned)
        
        if alert.urgency_score < 3 and not mentioned_high_value:
            return False
            
        # Add to sent alerts
        self.sent_alerts.add(alert_id)
        
        # Clean old alerts (keep only last 1000)
        if len(self.sent_alerts) > 1000:
            # Remove oldest 200 alerts (simple cleanup)
            alerts_list = list(self.sent_alerts)
            self.sent_alerts = set(alerts_list[-800:])
            
        return True
        
    def send_alert(self, alert: NewsAlert) -> bool:
        """Send alert via Telegram"""
        try:
            message = self.format_alert_message(alert)
            
            # Use urgent flag for high urgency alerts
            urgent = alert.urgency_score >= 7
            
            return self.telegram_bot.send_alert(message, urgent=urgent)
            
        except Exception as e:
            print(f"Error sending alert: {e}")
            return False
            
    def monitor_cycle(self):
        """Single monitoring cycle"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for news...")
            
            alerts = self.get_all_news()
            
            alerts_sent = 0
            for alert in alerts:
                if self.should_send_alert(alert):
                    success = self.send_alert(alert)
                    if success:
                        alerts_sent += 1
                        print(f"Alert sent: {alert.title[:50]}... (Urgency: {alert.urgency_score})")
                    
                    # Rate limiting - don't spam
                    time.sleep(2)
                    
            if alerts_sent == 0:
                print("No new alerts to send")
                
        except Exception as e:
            print(f"Error in monitoring cycle: {e}")
            
    def start_monitoring(self, interval_minutes: int = 5):
        """Start continuous monitoring"""
        print(f"Starting flash news monitoring...")
        print(f"Monitoring {len(self.monitored_symbols)} symbols")
        print(f"Check interval: {interval_minutes} minutes")
        print(f"Telegram bot connected: {self.telegram_bot.chat_id}")
        
        # Send startup message
        startup_msg = f"Flash News Monitor Started!\n\nMonitoring {len(self.monitored_symbols)} stocks\nCheck interval: {interval_minutes} min\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.telegram_bot.send_message(startup_msg)
        
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    self.monitor_cycle()
                    time.sleep(interval_minutes * 60)  # Convert to seconds
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error in monitor loop: {e}")
                    time.sleep(30)  # Wait 30 seconds before retrying
                    
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        print("Stopping news monitoring...")
        self.running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
        # Send shutdown message
        shutdown_msg = f"Flash News Monitor Stopped\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.telegram_bot.send_message(shutdown_msg)
        
    def test_alert_system(self):
        """Test the alert system with sample data"""
        print("Testing alert system...")
        
        print("Getting real news for test alerts...")
        
        # Get actual news alerts instead of dummy data
        real_alerts = self.get_all_news()
        
        if real_alerts:
            print(f"Found {len(real_alerts)} real news alerts")
            # Use the top 2 real alerts for testing
            test_alerts = real_alerts[:2]
        else:
            print("No real news found (likely due to rate limiting), creating realistic sample alerts...")
            # Create realistic test alerts with current financial topics
            test_alerts = [
                NewsAlert(
                    title="S&P 500 Hits New Record High on Strong Earnings Reports",
                    description="The S&P 500 index reached a new all-time high as major technology companies reported better-than-expected quarterly earnings, boosting investor confidence in the market.",
                    url="https://finance.yahoo.com/news/sp-500-record-high-earnings-reports",
                    source="Yahoo Finance",
                    published_at=datetime.now().isoformat(),
                    symbols_mentioned=["SPY", "AAPL", "MSFT"],
                    urgency_score=6,
                    keywords_matched=["record high", "strong earnings"]
                ),
                NewsAlert(
                    title="Federal Reserve Officials Signal Potential Rate Changes Ahead",
                    description="Federal Reserve officials indicated in recent speeches that interest rate adjustments may be considered based on upcoming economic data and inflation trends.",
                    url="https://finance.yahoo.com/news/federal-reserve-rate-changes-ahead",
                    source="Yahoo Finance",
                    published_at=datetime.now().isoformat(),
                    symbols_mentioned=["SPY"],
                    urgency_score=8,
                    keywords_matched=["federal reserve", "interest rate"]
                )
            ]
        
        for alert in test_alerts:
            success = self.send_alert(alert)
            print(f"Test alert sent: {'SUCCESS' if success else 'FAILED'}")
            time.sleep(3)


def main():
    """Main function to run the flash news monitor"""
    # Configuration - Update these with your credentials
    BOT_TOKEN = "8060365740:AAHBifQY747PaIfTjG39N2kdoLRUJXlDN9M"
    CHAT_ID = "5722055278"
    NEWS_API_KEY = None  # Optional: Add your NewsAPI key for more comprehensive news
    
    # Create monitor instance
    monitor = FlashNewsMonitor(BOT_TOKEN, CHAT_ID, NEWS_API_KEY)
    
    # Add additional symbols to monitor (optional)
    additional_symbols = ["SPY", "QQQ", "IWM", "VIX"]  # ETFs and volatility index
    monitor.add_monitored_symbols(additional_symbols)
    
    print("Flash News Monitor")
    print("=" * 30)
    print("1. Test alert system")
    print("2. Start monitoring (5 min intervals)")
    print("3. Start monitoring (1 min intervals) - High frequency")
    print("4. Run single news check")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        monitor.test_alert_system()
        
    elif choice == "2":
        try:
            monitor.start_monitoring(interval_minutes=5)
            print("Monitoring started. Press Ctrl+C to stop...")
            
            # Keep main thread alive
            while monitor.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            
    elif choice == "3":
        try:
            monitor.start_monitoring(interval_minutes=1)
            print("High-frequency monitoring started. Press Ctrl+C to stop...")
            
            # Keep main thread alive
            while monitor.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            
    elif choice == "4":
        monitor.monitor_cycle()
        
    elif choice == "5":
        print("Exiting...")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()