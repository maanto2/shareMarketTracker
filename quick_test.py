"""
Quick integration test for the market analysis system
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_basic_integration():
    """Test basic integration of all modules"""
    print("🧪 Running Quick Integration Test")
    print("=" * 40)
    
    try:
        # Test SP500Tracker
        print("\n1. Testing SP500Tracker...")
        from sp500_tracker import SP500Tracker
        tracker = SP500Tracker()
        
        # Test with just one stock to speed up
        perf = tracker.get_stock_performance('AAPL', '5d')
        if perf:
            print(f"✅ AAPL data: {perf['return_pct']:+.2f}% return")
        else:
            print("❌ Failed to get AAPL data")
        
        # Test EarningsCalendar
        print("\n2. Testing EarningsCalendar...")
        from earnings_calendar import EarningsCalendar
        earnings = EarningsCalendar()
        
        # This will likely fail without API key, but that's expected
        earnings_data = earnings.get_company_earnings_info(['AAPL'])
        if earnings_data:
            print("✅ Earnings calendar working")
        else:
            print("⚠️ Earnings calendar needs API key (expected)")
        
        # Test SentimentAnalyzer
        print("\n3. Testing SentimentAnalyzer...")
        from sentiment_analyzer import SentimentAnalyzer
        sentiment = SentimentAnalyzer()
        
        # This will likely fail without API key, but that's expected
        test_companies = [{'symbol': 'AAPL', 'sector': 'Technology'}]
        sentiment_data = sentiment.analyze_multiple_companies(test_companies)
        if sentiment_data:
            print("✅ Sentiment analyzer working")
        else:
            print("⚠️ Sentiment analyzer needs API key (expected)")
        
        # Test MarketOrchestrator
        print("\n4. Testing MarketOrchestrator...")
        from market_orchestrator import MarketAnalysisOrchestrator
        orchestrator = MarketAnalysisOrchestrator()
        
        # Test quick analysis with just AAPL
        quick_results = orchestrator.run_quick_analysis(['AAPL'])
        if quick_results and quick_results['performance_data']:
            print("✅ Market orchestrator working")
            print(f"   AAPL return: {quick_results['performance_data'][0]['return_pct']:+.2f}%")
        else:
            print("❌ Market orchestrator failed")
        
        print("\n🎉 Integration test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_integration()