"""
Sentiment Analysis Module
Analyzes news sentiment for top performing companies using NLP
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import re
from collections import Counter
import time

class SentimentAnalyzer:
    def __init__(self, news_api_key: str = None):
        """
        Initialize sentiment analyzer
        
        Args:
            news_api_key: Optional NewsAPI key for news fetching
        """
        self.news_api_key = news_api_key
        
        # Simple sentiment words (can be expanded or replaced with ML models)
        self.positive_words = {
            'excellent', 'amazing', 'outstanding', 'superb', 'fantastic', 'great', 'good',
            'positive', 'growth', 'profit', 'gain', 'increase', 'up', 'rise', 'surge',
            'bull', 'bullish', 'strong', 'robust', 'solid', 'beat', 'exceed', 'outperform',
            'buy', 'upgrade', 'recommend', 'boost', 'rally', 'momentum', 'optimistic'
        }
        
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'poor', 'negative', 'loss', 'decline',
            'decrease', 'down', 'fall', 'drop', 'bear', 'bearish', 'weak', 'fragile',
            'miss', 'underperform', 'sell', 'downgrade', 'concern', 'worry', 'crash',
            'plunge', 'pessimistic', 'risk', 'threat', 'problem', 'issue', 'struggle'
        }
    
    def _generate_trading_recommendation(self, sentiment: str, score: float, confidence: float) -> Dict[str, str]:
        """Generate trading recommendation based on sentiment analysis"""
        # Strong recommendations require high confidence (>70%) and clear sentiment
        if confidence >= 70:
            if sentiment == 'positive' and score > 1.5:
                return {
                    'action': 'BUY',
                    'strength': 'STRONG',
                    'reason': f'Strong positive sentiment (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
            elif sentiment == 'positive' and score > 0.5:
                return {
                    'action': 'BUY',
                    'strength': 'MODERATE',
                    'reason': f'Positive sentiment (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
            elif sentiment == 'negative' and score < -1.5:
                return {
                    'action': 'SELL',
                    'strength': 'STRONG',
                    'reason': f'Strong negative sentiment (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
            elif sentiment == 'negative' and score < -0.5:
                return {
                    'action': 'SELL',
                    'strength': 'MODERATE',
                    'reason': f'Negative sentiment (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
        
        # Weak recommendations for moderate confidence (50-70%)
        elif confidence >= 50:
            if sentiment == 'positive' and score > 1.0:
                return {
                    'action': 'BUY',
                    'strength': 'WEAK',
                    'reason': f'Cautious positive outlook (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
            elif sentiment == 'negative' and score < -1.0:
                return {
                    'action': 'SELL',
                    'strength': 'WEAK',
                    'reason': f'Cautious negative outlook (score: {score:.2f}, confidence: {confidence:.1f}%)'
                }
        
        # Default: HOLD for uncertain sentiment
        return {
            'action': 'HOLD',
            'strength': 'NEUTRAL',
            'reason': f'Mixed or uncertain sentiment (score: {score:.2f}, confidence: {confidence:.1f}%)'
        }
    
    def get_company_news(self, symbol: str, company_name: str = None, days_back: int = 7) -> List[Dict]:
        """Get news articles for a company"""
        news_articles = []
        
        # Try NewsAPI if key is available
        if self.news_api_key:
            news_articles.extend(self._get_news_from_newsapi(symbol, company_name, days_back))
        
        # Try free news sources
        news_articles.extend(self._get_news_from_free_sources(symbol, company_name, days_back))
        
        return news_articles
    
    def _get_news_from_newsapi(self, symbol: str, company_name: str, days_back: int) -> List[Dict]:
        """Get news from NewsAPI (requires API key)"""
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            # Create search query
            query_terms = [symbol]
            if company_name:
                query_terms.append(f'"{company_name}"')
            
            query = ' OR '.join(query_terms)
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.news_api_key,
                'pageSize': 20
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            articles = []
            if data.get('status') == 'ok':
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'NewsAPI'),
                        'url': article.get('url', '')
                    })
            
            return articles
            
        except Exception as e:
            print(f"Error getting news from NewsAPI for {symbol}: {e}")
            return []
    
    def _get_news_from_free_sources(self, symbol: str, company_name: str, days_back: int) -> List[Dict]:
        """Get news from free sources (limited functionality)"""
        articles = []
        
        try:
            # Try Yahoo Finance RSS (basic)
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Basic RSS parsing (would need proper XML parser for production)
                content = response.text
                
                # Extract titles (very basic approach)
                title_matches = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
                
                for i, title in enumerate(title_matches[:5]):  # Limit results
                    articles.append({
                        'title': title,
                        'description': '',
                        'content': '',
                        'published_at': datetime.now().isoformat(),
                        'source': 'Yahoo Finance RSS',
                        'url': f'https://finance.yahoo.com/quote/{symbol}'
                    })
            
        except Exception as e:
            print(f"Error getting free news for {symbol}: {e}")
        
        return articles
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a text using simple word-based approach"""
        if not text:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        # Clean and tokenize text
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Count positive and negative words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Calculate sentiment score
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        score = (positive_count - negative_count) / len(words) * 100
        confidence = total_sentiment_words / len(words) * 100
        
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
            'confidence': min(confidence, 100),
            'positive_words': positive_count,
            'negative_words': negative_count,
            'total_words': len(words)
        }
    
    def analyze_company_sentiment(self, symbol: str, company_name: str = None) -> Dict:
        """Analyze overall sentiment for a company based on recent news"""
        print(f"Analyzing sentiment for {symbol}...")
        
        # Get news articles
        articles = self.get_company_news(symbol, company_name)
        
        if not articles:
            return {
                'symbol': symbol,
                'overall_sentiment': 'neutral',
                'overall_score': 0,
                'confidence': 0,
                'articles_analyzed': 0,
                'sentiment_breakdown': {'positive': 0, 'negative': 0, 'neutral': 0}
            }
        
        # Analyze sentiment for each article
        article_sentiments = []
        sentiment_scores = []
        
        for article in articles:
            # Combine title and description for analysis
            text = f"{article.get('title', '')} {article.get('description', '')}"
            sentiment = self.analyze_text_sentiment(text)
            
            article_sentiments.append(sentiment['sentiment'])
            sentiment_scores.append(sentiment['score'])
            
            # Add sentiment to article
            article['sentiment_analysis'] = sentiment
        
        # Calculate overall sentiment
        sentiment_counts = Counter(article_sentiments)
        avg_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # Determine overall sentiment
        if avg_score > 1:
            overall_sentiment = 'positive'
        elif avg_score < -1:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        # Calculate confidence based on consistency
        most_common_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral'
        confidence = sentiment_counts[most_common_sentiment] / len(article_sentiments) * 100 if article_sentiments else 0
        
        # Generate trading recommendation
        trading_recommendation = self._generate_trading_recommendation(
            overall_sentiment, avg_score, confidence
        )
        
        return {
            'symbol': symbol,
            'company_name': company_name,
            'overall_sentiment': overall_sentiment,
            'overall_score': avg_score,
            'confidence': confidence,
            'trading_recommendation': trading_recommendation,
            'articles_analyzed': len(articles),
            'sentiment_breakdown': dict(sentiment_counts),
            'articles': articles[:5],  # Include top 5 articles
            'analysis_date': datetime.now().isoformat()
        }
    
    def analyze_multiple_companies(self, companies: List[Dict]) -> List[Dict]:
        """Analyze sentiment for multiple companies"""
        results = []
        
        for i, company in enumerate(companies):
            symbol = company.get('symbol')
            company_name = company.get('company_name', company.get('longName'))
            
            print(f"Processing {symbol} ({i+1}/{len(companies)})")
            
            sentiment_result = self.analyze_company_sentiment(symbol, company_name)
            
            # Merge with original company data
            combined_result = {**company, **sentiment_result}
            results.append(combined_result)
            
            # Rate limiting
            time.sleep(1)
        
        return results
    
    def get_sentiment_summary(self, sentiment_results: List[Dict]) -> str:
        """Generate a summary of sentiment analysis results"""
        if not sentiment_results:
            return "No sentiment data available"
        
        # Count sentiments
        sentiment_counts = Counter(result['overall_sentiment'] for result in sentiment_results)
        
        summary = f"\n🧠 SENTIMENT ANALYSIS SUMMARY\n"
        summary += "=" * 40 + "\n"
        summary += f"Companies analyzed: {len(sentiment_results)}\n"
        summary += f"Positive sentiment: {sentiment_counts.get('positive', 0)}\n"
        summary += f"Negative sentiment: {sentiment_counts.get('negative', 0)}\n"
        summary += f"Neutral sentiment: {sentiment_counts.get('neutral', 0)}\n\n"
        
        # Show companies by sentiment
        for sentiment_type in ['positive', 'negative', 'neutral']:
            companies = [r for r in sentiment_results if r['overall_sentiment'] == sentiment_type]
            if companies:
                emoji = {'positive': '😊', 'negative': '😞', 'neutral': '😐'}[sentiment_type]
                summary += f"{emoji} {sentiment_type.upper()} SENTIMENT:\n"
                
                for company in companies[:5]:  # Top 5
                    symbol = company['symbol']
                    score = company['overall_score']
                    confidence = company['confidence']
                    articles = company['articles_analyzed']
                    
                    summary += f"  {symbol}: Score {score:+.2f}, "
                    summary += f"Confidence {confidence:.1f}%, "
                    summary += f"{articles} articles\n"
                
                summary += "\n"
        
        return summary
    
    def save_sentiment_analysis(self, results: List[Dict], filename: str = None) -> str:
        """Save sentiment analysis results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_analysis_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'companies_analyzed': len(results),
            'results': results
        }
        
        filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Sentiment analysis saved to: {filepath}")
        return filepath

def main():
    """Main function to demonstrate sentiment analysis"""
    # Initialize analyzer (add NewsAPI key if you have one)
    analyzer = SentimentAnalyzer(news_api_key=None)
    
    # Test companies
    test_companies = [
        {'symbol': 'AAPL', 'company_name': 'Apple Inc.'},
        {'symbol': 'MSFT', 'company_name': 'Microsoft Corporation'},
        {'symbol': 'GOOGL', 'company_name': 'Alphabet Inc.'},
        {'symbol': 'TSLA', 'company_name': 'Tesla Inc.'}
    ]
    
    # Analyze sentiment
    results = analyzer.analyze_multiple_companies(test_companies)
    
    # Save results
    analyzer.save_sentiment_analysis(results)
    
    # Print summary
    summary = analyzer.get_sentiment_summary(results)
    print(summary)

if __name__ == "__main__":
    main()