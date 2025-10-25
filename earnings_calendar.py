"""
Earnings Calendar Fetcher
Gets quarterly earnings dates for companies using multiple financial APIs
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import time

class EarningsCalendar:
    def __init__(self, alpha_vantage_key: str = None):
        """
        Initialize earnings calendar fetcher
        
        Args:
            alpha_vantage_key: Optional Alpha Vantage API key for additional data
        """
        self.alpha_vantage_key = alpha_vantage_key
        
    def get_earnings_date_yfinance(self, symbol: str) -> Dict:
        """Get earnings date using yfinance"""
        try:
            stock = yf.Ticker(symbol)
            
            # Get earnings dates (calendar)
            calendar = stock.calendar
            next_earnings = None
            
            if calendar is not None and isinstance(calendar, dict):
                # Extract earnings date from calendar dict
                if 'Earnings Date' in calendar:
                    earnings_date = calendar['Earnings Date']
                    if isinstance(earnings_date, list) and earnings_date:
                        earnings_date_obj = earnings_date[0]
                        # Check if it's a future date
                        from datetime import date
                        today = date.today()
                        
                        if isinstance(earnings_date_obj, date):
                            if earnings_date_obj > today:
                                next_earnings = earnings_date_obj.strftime('%Y-%m-%d')
            elif calendar is not None and hasattr(calendar, 'empty') and not calendar.empty:
                # Fallback to old method if calendar is a DataFrame
                next_earnings = calendar.index[0].strftime('%Y-%m-%d')
            
            # Get basic company info
            info = stock.info
            company_name = info.get('longName', symbol)
            sector = info.get('sector', 'Unknown')
            
            # Get earnings history for pattern analysis
            earnings_hist = stock.earnings_dates
            past_earnings = []
            if earnings_hist is not None and hasattr(earnings_hist, 'empty') and not earnings_hist.empty:
                past_earnings = earnings_hist.head(4).index.strftime('%Y-%m-%d').tolist()
            
            return {
                'symbol': symbol,
                'company_name': company_name,
                'sector': sector,
                'next_earnings_date': next_earnings,
                'past_earnings_dates': past_earnings,
                'source': 'yfinance'
            }
            
        except Exception as e:
            print(f"Error getting earnings for {symbol} from yfinance: {e}")
            return None
    
    def get_earnings_date_alphavantage(self, symbol: str) -> Dict:
        """Get earnings date using Alpha Vantage API"""
        if not self.alpha_vantage_key:
            return None
            
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'EARNINGS',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'quarterlyEarnings' in data:
                quarterly = data['quarterlyEarnings']
                if quarterly:
                    # Get the most recent/next earnings
                    latest = quarterly[0]
                    return {
                        'symbol': symbol,
                        'next_earnings_date': latest.get('reportedDate'),
                        'estimated_eps': latest.get('estimatedEPS'),
                        'reported_eps': latest.get('reportedEPS'),
                        'source': 'alphavantage'
                    }
            
        except Exception as e:
            print(f"Error getting earnings for {symbol} from Alpha Vantage: {e}")
            
        return None
    
    def get_earnings_calendar_fmp(self, from_date: str = None, to_date: str = None) -> List[Dict]:
        """
        Get earnings calendar from Financial Modeling Prep (free tier)
        Note: This is a free API but has limitations
        """
        try:
            if not from_date:
                from_date = datetime.now().strftime('%Y-%m-%d')
            if not to_date:
                to_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Free endpoint (limited)
            url = f"https://financialmodelingprep.com/api/v3/earning_calendar"
            params = {
                'from': from_date,
                'to': to_date
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            earnings_list = []
            for item in data:
                earnings_list.append({
                    'symbol': item.get('symbol'),
                    'company_name': item.get('name'),
                    'earnings_date': item.get('date'),
                    'estimated_eps': item.get('epsEstimated'),
                    'revenue_estimated': item.get('revenueEstimated'),
                    'source': 'fmp'
                })
            
            return earnings_list
            
        except Exception as e:
            print(f"Error getting earnings calendar from FMP: {e}")
            return []
    
    def get_company_earnings_info(self, symbols: List[str]) -> List[Dict]:
        """Get earnings information for a list of companies"""
        earnings_info = []
        
        print(f"Getting earnings information for {len(symbols)} companies...")
        
        for i, symbol in enumerate(symbols):
            print(f"Processing {symbol} ({i+1}/{len(symbols)})")
            
            # Try yfinance first
            earnings_data = self.get_earnings_date_yfinance(symbol)
            
            # If Alpha Vantage key is available, try to get additional data
            if self.alpha_vantage_key:
                av_data = self.get_earnings_date_alphavantage(symbol)
                if av_data and earnings_data:
                    # Merge data from both sources
                    earnings_data.update({
                        'estimated_eps': av_data.get('estimated_eps'),
                        'reported_eps': av_data.get('reported_eps')
                    })
            
            if earnings_data:
                earnings_info.append(earnings_data)
            
            # Rate limiting
            time.sleep(0.5)
        
        return earnings_info
    
    def filter_upcoming_earnings(self, 
                                earnings_info: List[Dict], 
                                days_ahead: int = 30) -> List[Dict]:
        """Filter companies with earnings in the next N days"""
        upcoming = []
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        for company in earnings_info:
            earnings_date_str = company.get('next_earnings_date')
            if earnings_date_str:
                try:
                    earnings_date = datetime.strptime(earnings_date_str, '%Y-%m-%d')
                    if datetime.now() <= earnings_date <= cutoff_date:
                        days_until = (earnings_date - datetime.now()).days
                        company['days_until_earnings'] = days_until
                        upcoming.append(company)
                except ValueError:
                    continue
        
        # Sort by days until earnings
        upcoming.sort(key=lambda x: x.get('days_until_earnings', 999))
        return upcoming
    
    def save_earnings_calendar(self, earnings_info: List[Dict], filename: str = None) -> str:
        """Save earnings calendar to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"earnings_calendar_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'companies': earnings_info
        }
        
        filepath = f"c:\\Users\\Martin\\Desktop\\Py_coding\\Share_market\\{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Earnings calendar saved to: {filepath}")
        return filepath
    
    def generate_earnings_summary(self, upcoming_earnings: List[Dict]) -> str:
        """Generate a formatted summary of upcoming earnings"""
        if not upcoming_earnings:
            return "No upcoming earnings found"
        
        summary = f"\nUPCOMING EARNINGS ({len(upcoming_earnings)} companies)\n"
        summary += "=" * 60 + "\n"
        
        for company in upcoming_earnings:
            symbol = company.get('symbol', 'N/A')
            name = company.get('company_name', 'Unknown')
            date = company.get('next_earnings_date', 'N/A')
            days = company.get('days_until_earnings', 'N/A')
            sector = company.get('sector', 'Unknown')
            
            summary += f"{symbol:5s} | {name[:25]:25s} | {date} | "
            summary += f"in {days:2d} days | {sector}\n"
        
        return summary

def main():
    """Main function to demonstrate the earnings calendar"""
    # Initialize (add your Alpha Vantage key here if you have one)
    calendar = EarningsCalendar(alpha_vantage_key=None)
    
    # Example: Get earnings for some top companies
    test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM']
    
    # Get earnings information
    earnings_info = calendar.get_company_earnings_info(test_symbols)
    
    # Filter for upcoming earnings (next 30 days)
    upcoming = calendar.filter_upcoming_earnings(earnings_info, days_ahead=30)
    
    # Save to file
    if earnings_info:
        calendar.save_earnings_calendar(earnings_info)
    
    # Print summary
    if upcoming:
        summary = calendar.generate_earnings_summary(upcoming)
        print(summary)
    else:
        print("No upcoming earnings found for the selected companies")

if __name__ == "__main__":
    main()