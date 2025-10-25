"""
Simple test script to verify the market analysis system
"""

import sys
import os

# Test basic imports
try:
    import yfinance as yf
    import pandas as pd
    import requests
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test yfinance functionality
try:
    print("\n📊 Testing yfinance with AAPL...")
    stock = yf.Ticker('AAPL')
    hist = stock.history(period='5d')
    if not hist.empty:
        print(f"✅ Successfully retrieved {len(hist)} days of AAPL data")
        print(f"Latest close price: ${hist['Close'].iloc[-1]:.2f}")
    else:
        print("❌ No data retrieved from yfinance")
except Exception as e:
    print(f"❌ yfinance error: {e}")

# Test S&P 500 list fetching
try:
    print("\n📈 Testing S&P 500 list fetching...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    symbols = sp500_table['Symbol'].tolist()
    print(f"✅ Successfully loaded {len(symbols)} S&P 500 symbols")
    print(f"First 5 symbols: {symbols[:5]}")
except Exception as e:
    print(f"❌ S&P 500 fetching error: {e}")

# Test our modules
try:
    print("\n🚀 Testing our custom modules...")
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    from sp500_tracker import SP500Tracker
    
    tracker = SP500Tracker()
    print(f"✅ SP500Tracker initialized with {len(tracker.sp500_symbols)} symbols")
    
    # Test getting performance for a single stock
    print("\n📊 Testing single stock performance analysis...")
    perf_data = tracker.get_stock_performance('AAPL', period='1mo')
    if perf_data:
        print(f"✅ AAPL performance data retrieved:")
        print(f"   Return: {perf_data['return_pct']:+.2f}%")
        print(f"   Current price: ${perf_data['end_price']:.2f}")
        print(f"   Sector: {perf_data['sector']}")
    else:
        print("❌ Could not retrieve AAPL performance data")
        
except Exception as e:
    print(f"❌ Module testing error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Test completed!")