#!/usr/bin/env python3
"""
Test script for the Stock Analyzer components
"""

from stock_analyzer import StockAnalyzer
from prediction_engine import PredictionEngine

def test_stock_analysis():
    """Test stock analysis with a sample stock"""
    print("🧪 TESTING STOCK ANALYZER")
    print("=" * 40)
    
    # Test with Apple stock
    analyzer = StockAnalyzer()
    print("📊 Analyzing AAPL...")
    
    try:
        # Analyze AAPL
        result = analyzer.analyze_stock('AAPL')
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Analysis successful!")
        print(f"💰 Current Price: ${result.get('current_price', 0):.2f}")
        print(f"🏢 Company: {result.get('company_name', 'Unknown')}")
        
        # Test technical analysis
        tech = result.get('technical_analysis', {})
        if tech and not tech.get('error'):
            print(f"📈 Day Change: {tech.get('day_change_pct', 0):+.2f}%")
            print(f"📊 RSI: {tech.get('rsi', 0):.1f}")
            print(f"📊 Volume Ratio: {tech.get('volume_ratio', 0):.2f}x")
        
        # Test sentiment analysis
        sentiment = result.get('sentiment_analysis', {})
        if sentiment and not sentiment.get('error'):
            print(f"📰 Sentiment: {sentiment.get('overall_sentiment', 'unknown').upper()}")
            print(f"📄 Articles: {sentiment.get('articles_analyzed', 0)}")
        
        # Test prediction engine
        print("\n🔮 Testing Prediction Engine...")
        engine = PredictionEngine()
        prediction = engine.get_prediction(result)
        
        rec = prediction.get('recommendation', {})
        print(f"🎯 Recommendation: {rec.get('action', 'UNKNOWN')}")
        print(f"📈 Confidence: {rec.get('confidence', 0):.1f}%")
        print(f"💡 Reason: {rec.get('reason', 'No reason provided')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_multiple_stocks():
    """Test with multiple stocks"""
    print("\n🧪 TESTING MULTIPLE STOCKS")
    print("=" * 40)
    
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    analyzer = StockAnalyzer()
    engine = PredictionEngine()
    
    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}...")
        try:
            result = analyzer.analyze_stock(symbol)
            if not result.get('error'):
                prediction = engine.get_prediction(result)
                rec = prediction.get('recommendation', {})
                
                print(f"  💰 Price: ${result.get('current_price', 0):.2f}")
                print(f"  🎯 Action: {rec.get('action', 'UNKNOWN')}")
                print(f"  📈 Confidence: {rec.get('confidence', 0):.1f}%")
            else:
                print(f"  ❌ Error: {result['error']}")
        except Exception as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 STOCK ANALYZER TEST SUITE")
    print("=" * 50)
    
    # Test basic functionality
    success = test_stock_analysis()
    
    if success:
        print("\n✅ Basic test passed!")
        test_multiple_stocks()
        print("\n🎉 All tests completed!")
        print("\n📝 NEXT STEPS:")
        print("1. Set up your Telegram bot token and chat ID")
        print("2. Run: python main.py")
        print("3. Start chatting with your bot!")
    else:
        print("\n❌ Basic test failed. Please check your internet connection.")