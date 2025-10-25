"""
S&P 500 Top Performers Tracker
Fetches and ranks S&P 500 companies by various performance metrics
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
from typing import List, Dict, Tuple
import time

class SP500Tracker:
    def __init__(self):
        self.sp500_symbols = self._get_sp500_symbols()
        
    def _get_sp500_symbols(self) -> List[str]:
        """Get S&P 500 symbols from Wikipedia"""
        try:
            # Get S&P 500 list from Wikipedia
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            tables = pd.read_html(url)
            sp500_table = tables[0]
            symbols = sp500_table['Symbol'].tolist()
            print(f"Loaded {len(symbols)} S&P 500 symbols")
            return symbols
        except Exception as e:
            print(f"Error fetching S&P 500 symbols: {e}")
            # Fallback to some major companies
            return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'JNJ', 'V']
    
    def get_stock_performance(self, symbol: str, period: str = "1mo") -> Dict:
        """Get performance metrics for a single stock"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            
            if hist.empty:
                return None
                
            # Calculate performance metrics
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            return_pct = ((end_price - start_price) / start_price) * 100
            
            # Volume metrics
            avg_volume = hist['Volume'].mean()
            recent_volume = hist['Volume'].iloc[-1]
            volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 0
            
            # Volatility
            volatility = hist['Close'].pct_change().std() * 100
            
            # Get basic info
            info = stock.info
            market_cap = info.get('marketCap', 0)
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            return {
                'symbol': symbol,
                'return_pct': return_pct,
                'start_price': start_price,
                'end_price': end_price,
                'avg_volume': avg_volume,
                'recent_volume': recent_volume,
                'volume_ratio': volume_ratio,
                'volatility': volatility,
                'market_cap': market_cap,
                'sector': sector,
                'industry': industry
            }
            
        except Exception as e:
            print(f"Error getting data for {symbol}: {e}")
            return None
    
    def get_top_performers(self, 
                          metric: str = 'return_pct', 
                          top_n: int = 20, 
                          period: str = "1mo",
                          min_market_cap: int = 1000000000) -> pd.DataFrame:
        """Get top performing stocks based on specified metric"""
        
        print(f"Analyzing {len(self.sp500_symbols)} S&P 500 stocks...")
        performance_data = []
        
        # Process stocks in batches to avoid rate limiting
        batch_size = 10
        for i in range(0, len(self.sp500_symbols), batch_size):
            batch = self.sp500_symbols[i:i+batch_size]
            
            for symbol in batch:
                data = self.get_stock_performance(symbol, period)
                if data and data['market_cap'] >= min_market_cap:
                    performance_data.append(data)
            
            # Sleep to avoid rate limiting
            if i < len(self.sp500_symbols) - batch_size:
                time.sleep(1)
            
            print(f"Processed {min(i+batch_size, len(self.sp500_symbols))}/{len(self.sp500_symbols)} stocks")
        
        # Create DataFrame and sort by metric
        df = pd.DataFrame(performance_data)
        if df.empty:
            return df
            
        # Sort by the specified metric (descending for positive metrics)
        ascending = metric in ['volatility']  # Lower volatility is better
        df_sorted = df.sort_values(by=metric, ascending=ascending)
        
        return df_sorted.head(top_n)
    
    def save_top_performers(self, 
                           df: pd.DataFrame, 
                           filename: str = None,
                           metric: str = 'return_pct') -> str:
        """Save top performers to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"top_performers_{metric}_{timestamp}.json"
        
        # Convert DataFrame to dict for JSON serialization
        data = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric,
            'companies': df.to_dict('records')
        }
        
        filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Top performers saved to: {filepath}")
        return filepath
    
    def get_performance_summary(self, df: pd.DataFrame, metric: str) -> str:
        """Generate a summary of top performers"""
        if df.empty:
            return "No data available"
        
        summary = f"\n🏆 TOP {len(df)} PERFORMERS BY {metric.upper()}\n"
        summary += "=" * 50 + "\n"
        
        for idx, row in df.iterrows():
            summary += f"{idx+1:2d}. {row['symbol']:5s} | "
            summary += f"{row[metric]:8.2f}% | "
            summary += f"${row['end_price']:8.2f} | "
            summary += f"{row['sector']}\n"
        
        return summary

def main():
    """Main function to demonstrate the tracker"""
    tracker = SP500Tracker()
    
    # Get top performers by different metrics
    metrics = ['return_pct', 'volume_ratio', 'volatility']
    
    for metric in metrics:
        print(f"\n--- Getting top performers by {metric} ---")
        top_performers = tracker.get_top_performers(
            metric=metric, 
            top_n=10, 
            period="1mo"
        )
        
        if not top_performers.empty:
            # Save to file
            filepath = tracker.save_top_performers(top_performers, metric=metric)
            
            # Print summary
            summary = tracker.get_performance_summary(top_performers, metric)
            print(summary)
        else:
            print(f"No data available for {metric}")

if __name__ == "__main__":
    main()