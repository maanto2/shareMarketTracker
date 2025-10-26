#!/usr/bin/env python3
"""
Stock Analyzer Module
Performs comprehensive technical analysis and news sentiment for individual stocks
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

class StockAnalyzer:
    def __init__(self, news_api_key: Optional[str] = None):
        """
        Initialize Stock Analyzer
        
        Args:
            news_api_key: Optional NewsAPI key for enhanced news analysis
        """
        self.news_api_key = news_api_key
        
        # Sentiment word lists
        self.positive_words = {
            'excellent', 'amazing', 'outstanding', 'superb', 'fantastic', 'great', 'good',
            'positive', 'growth', 'profit', 'gain', 'increase', 'up', 'rise', 'surge',
            'bull', 'bullish', 'strong', 'robust', 'solid', 'beat', 'exceed', 'outperform',
            'buy', 'upgrade', 'recommend', 'boost', 'rally', 'momentum', 'optimistic',
            'breakthrough', 'success', 'winning', 'recovery', 'expansion'
        }
        
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'poor', 'negative', 'loss', 'decline',
            'decrease', 'down', 'fall', 'drop', 'bear', 'bearish', 'weak', 'fragile',
            'miss', 'underperform', 'sell', 'downgrade', 'concern', 'worry', 'crash',
            'plunge', 'pessimistic', 'risk', 'threat', 'problem', 'issue', 'struggle',
            'bankruptcy', 'lawsuit', 'investigation', 'scandal', 'crisis'
        }
    
    def analyze_stock(self, symbol: str) -> Dict:
        """
        Perform comprehensive stock analysis
        
        Args:
            symbol: Stock symbol to analyze
            
        Returns:
            Dictionary containing all analysis results
        """
        try:
            print(f"🔍 Starting analysis for {symbol}")
            
            # Get basic stock data
            stock_data = self.get_stock_data(symbol)
            if not stock_data or stock_data.get('error'):
                return stock_data
            
            # Perform technical analysis
            technical_analysis = self.perform_technical_analysis(symbol)
            
            # Perform sentiment analysis
            sentiment_analysis = self.perform_sentiment_analysis(symbol, stock_data.get('company_name'))
            
            # Combine all results
            analysis_result = {
                'symbol': symbol.upper(),
                'analysis_timestamp': datetime.now().isoformat(),
                **stock_data,
                'technical_analysis': technical_analysis,
                'sentiment_analysis': sentiment_analysis
            }
            
            print(f"✅ Analysis complete for {symbol}")
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            return {
                'symbol': symbol.upper(),
                'error': f'Analysis failed: {str(e)}',
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def get_stock_data(self, symbol: str) -> Dict:
        """Get basic stock data and company information"""
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get basic info
            info = ticker.info
            
            # Get current price and basic metrics
            hist = ticker.history(period="5d")
            if hist.empty:
                return {'error': f'No data found for symbol {symbol}'}
            
            current_price = hist['Close'].iloc[-1]
            
            # Extract company information
            company_name = info.get('longName', info.get('shortName', 'Unknown Company'))
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE', 0)
            
            return {
                'current_price': float(current_price),
                'company_name': company_name,
                'market_data': {
                    'sector': sector,
                    'industry': industry,
                    'market_cap': market_cap,
                    'pe_ratio': pe_ratio,
                    'currency': info.get('currency', 'USD')
                }
            }
            
        except Exception as e:
            return {'error': f'Failed to get stock data: {str(e)}'}
    
    def perform_technical_analysis(self, symbol: str) -> Dict:
        """Perform technical analysis on the stock"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist_1d = ticker.history(period="5d", interval="1d")
            hist_1w = ticker.history(period="1mo", interval="1d")
            hist_1m = ticker.history(period="3mo", interval="1d")
            
            if hist_1d.empty:
                return {'error': 'No historical data available'}
            
            # Calculate price changes
            current_price = hist_1d['Close'].iloc[-1]
            
            # 1-day change
            day_change_pct = 0
            if len(hist_1d) >= 2:
                prev_price = hist_1d['Close'].iloc[-2]
                day_change_pct = ((current_price - prev_price) / prev_price) * 100
            
            # 1-week change
            week_change_pct = 0
            if len(hist_1w) >= 5:
                week_ago_price = hist_1w['Close'].iloc[-6] if len(hist_1w) >= 6 else hist_1w['Close'].iloc[0]
                week_change_pct = ((current_price - week_ago_price) / week_ago_price) * 100
            
            # 1-month change
            month_change_pct = 0
            if len(hist_1m) >= 20:
                month_ago_price = hist_1m['Close'].iloc[-21] if len(hist_1m) >= 21 else hist_1m['Close'].iloc[0]
                month_change_pct = ((current_price - month_ago_price) / month_ago_price) * 100
            
            # Volume analysis
            current_volume = hist_1d['Volume'].iloc[-1]
            avg_volume = hist_1w['Volume'].mean() if len(hist_1w) > 0 else current_volume
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Calculate RSI (14-period)
            rsi = self.calculate_rsi(hist_1m['Close']) if len(hist_1m) >= 14 else 50
            
            # Calculate moving averages
            ma_20 = hist_1m['Close'].tail(20).mean() if len(hist_1m) >= 20 else current_price
            ma_50 = hist_1m['Close'].tail(50).mean() if len(hist_1m) >= 50 else current_price
            
            # Price vs moving averages
            price_vs_ma20 = ((current_price - ma_20) / ma_20) * 100 if ma_20 > 0 else 0
            price_vs_ma50 = ((current_price - ma_50) / ma_50) * 100 if ma_50 > 0 else 0
            
            # Volatility (standard deviation of returns)
            returns = hist_1m['Close'].pct_change().dropna()
            volatility = returns.std() * 100 if len(returns) > 1 else 0
            
            return {
                'day_change_pct': day_change_pct,
                'week_change_pct': week_change_pct,
                'month_change_pct': month_change_pct,
                'volume_ratio': volume_ratio,
                'rsi': rsi,
                'price_vs_ma20': price_vs_ma20,
                'price_vs_ma50': price_vs_ma50,
                'volatility': volatility,
                'ma_20': ma_20,
                'ma_50': ma_50
            }
            
        except Exception as e:
            print(f"❌ Technical analysis error for {symbol}: {e}")
            return {'error': f'Technical analysis failed: {str(e)}'}
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI (Relative Strength Index)"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return float(rsi.iloc[-1]) if not rsi.empty else 50.0
        except:
            return 50.0  # Neutral RSI if calculation fails
    
    def perform_sentiment_analysis(self, symbol: str, company_name: str = None) -> Dict:
        """Perform news sentiment analysis"""
        try:
            print(f"📰 Getting news for {symbol}")
            
            # Get news articles
            news_articles = self.get_stock_news(symbol, company_name)
            
            if not news_articles:
                return {
                    'overall_sentiment': 'neutral',
                    'overall_score': 0,
                    'confidence': 0,
                    'articles_analyzed': 0,
                    'error': 'No news articles found'
                }
            
            # Analyze sentiment for each article
            sentiment_scores = []
            positive_articles = 0
            negative_articles = 0
            neutral_articles = 0
            
            for article in news_articles:
                # Combine title and description for analysis
                text = f"{article.get('title', '')} {article.get('description', '')}"
                sentiment = self.analyze_text_sentiment(text)
                
                sentiment_scores.append(sentiment['score'])
                
                # Count sentiment types
                if sentiment['sentiment'] == 'positive':
                    positive_articles += 1
                elif sentiment['sentiment'] == 'negative':
                    negative_articles += 1
                else:
                    neutral_articles += 1
            
            # Calculate overall sentiment
            overall_score = np.mean(sentiment_scores) if sentiment_scores else 0
            
            # Determine overall sentiment
            if overall_score > 1:
                overall_sentiment = 'positive'
            elif overall_score < -1:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            # Calculate confidence based on consistency
            total_articles = len(news_articles)
            if overall_sentiment == 'positive':
                confidence = (positive_articles / total_articles) * 100
            elif overall_sentiment == 'negative':
                confidence = (negative_articles / total_articles) * 100
            else:
                confidence = (neutral_articles / total_articles) * 100
            
            return {
                'overall_sentiment': overall_sentiment,
                'overall_score': overall_score,
                'confidence': confidence,
                'articles_analyzed': total_articles,
                'sentiment_breakdown': {
                    'positive': positive_articles,
                    'negative': negative_articles,
                    'neutral': neutral_articles
                },
                'recent_articles': news_articles[:3]  # Include top 3 articles
            }
            
        except Exception as e:
            print(f"❌ Sentiment analysis error for {symbol}: {e}")
            return {
                'overall_sentiment': 'neutral',
                'overall_score': 0,
                'confidence': 0,
                'articles_analyzed': 0,
                'error': f'Sentiment analysis failed: {str(e)}'
            }
    
    def get_stock_news(self, symbol: str, company_name: str = None, days_back: int = 7) -> List[Dict]:
        """Get recent news articles for a stock"""
        news_articles = []
        
        # Try NewsAPI if available
        if self.news_api_key:
            news_articles.extend(self._get_news_from_newsapi(symbol, company_name, days_back))
        
        # Try free sources
        news_articles.extend(self._get_news_from_free_sources(symbol, days_back))
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        for article in news_articles:
            title = article.get('title', '').lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles[:10]  # Return top 10 unique articles
    
    def _get_news_from_newsapi(self, symbol: str, company_name: str, days_back: int) -> List[Dict]:
        """Get news from NewsAPI"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            # Create search query
            query_terms = [symbol]
            if company_name:
                # Extract main company name (before "Inc.", "Corp.", etc.)
                main_name = company_name.split()[0]
                query_terms.append(f'"{main_name}"')
            
            query = ' OR '.join(query_terms)
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.news_api_key,
                'pageSize': 15
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            articles = []
            if data.get('status') == 'ok':
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'NewsAPI')
                    })
            
            return articles
            
        except Exception as e:
            print(f"❌ NewsAPI error for {symbol}: {e}")
            return []
    
    def _get_news_from_free_sources(self, symbol: str, days_back: int) -> List[Dict]:
        """Get news from free sources"""
        articles = []
        
        try:
            # Try Yahoo Finance RSS
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
            
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                content = response.text
                
                # Basic RSS parsing
                title_matches = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
                
                for title in title_matches[:8]:  # Limit results
                    if symbol.lower() in title.lower() or title.strip():
                        articles.append({
                            'title': title,
                            'description': '',
                            'url': f'https://finance.yahoo.com/quote/{symbol}/news',
                            'published_at': datetime.now().isoformat(),
                            'source': 'Yahoo Finance'
                        })
            
        except Exception as e:
            print(f"❌ Free news source error for {symbol}: {e}")
        
        return articles
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text using word-based approach"""
        if not text:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        # Clean and tokenize
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        # Count sentiment words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Calculate score
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        # Score calculation (normalized by text length)
        score = (positive_count - negative_count) / len(words) * 100
        
        # Confidence based on sentiment word density
        confidence = min((total_sentiment_words / len(words)) * 100, 100)
        
        # Determine sentiment category
        if score > 0.5:
            sentiment = 'positive'
        elif score < -0.5:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': confidence
        }

def main():
    """Test function"""
    analyzer = StockAnalyzer()
    
    # Test analysis
    test_symbols = ['AAPL', 'TSLA', 'MSFT']
    
    for symbol in test_symbols:
        print(f"\n{'='*50}")
        print(f"Testing analysis for {symbol}")
        print('='*50)
        
        result = analyzer.analyze_stock(symbol)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Analysis complete for {symbol}")
            print(f"📊 Current Price: ${result.get('current_price', 0):.2f}")
            print(f"🏢 Company: {result.get('company_name', 'Unknown')}")
            
            tech = result.get('technical_analysis', {})
            if tech and not tech.get('error'):
                print(f"📈 Day Change: {tech.get('day_change_pct', 0):+.2f}%")
                print(f"📊 RSI: {tech.get('rsi', 0):.1f}")
            
            sentiment = result.get('sentiment_analysis', {})
            if sentiment and not sentiment.get('error'):
                print(f"📰 Sentiment: {sentiment.get('overall_sentiment', 'unknown').upper()}")
                print(f"📄 Articles: {sentiment.get('articles_analyzed', 0)}")

if __name__ == "__main__":
    main()