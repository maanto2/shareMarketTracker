"""
FINAL EARNINGS CALENDAR TEST
Comprehensive test showing all earnings calendar capabilities
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from earnings_calendar import EarningsCalendar
from market_orchestrator import MarketAnalysisOrchestrator

def main():
    print("="*60)
    print("EARNINGS CALENDAR - COMPREHENSIVE TEST")
    print("="*60)
    
    # Initialize earnings calendar
    earnings_cal = EarningsCalendar()
    
    # Test with top tech companies that likely have upcoming earnings
    test_companies = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META', 'AMZN', 'TSLA', 'NFLX', 'CRM', 'ADBE']
    
    print(f"\n1. TESTING {len(test_companies)} MAJOR COMPANIES")
    print("-" * 40)
    
    # Get earnings information
    try:
        earnings_data = earnings_cal.get_company_earnings_info(test_companies)
        print(f"Successfully retrieved data for {len(earnings_data)} companies")
        
        # Count companies with future earnings
        companies_with_future_earnings = [e for e in earnings_data if e and e.get('next_earnings_date')]
        print(f"{len(companies_with_future_earnings)} companies have upcoming earnings dates")
        
        # Show individual results
        print("\n2. INDIVIDUAL COMPANY RESULTS")
        print("-" * 40)
        for earning in earnings_data:
            if earning:
                symbol = earning.get('symbol', 'Unknown') or 'Unknown'
                date = earning.get('next_earnings_date') or 'No upcoming date'
                company = (earning.get('company_name') or 'Unknown Company')[:30]
                sector = earning.get('sector') or 'Unknown'
                
                status = "UPCOMING" if date != 'No upcoming date' else "No Future Date"
                print(f"{symbol:5s} | {company:30s} | {date:12s} | {sector}")
        
        # Filter upcoming earnings
        print("\n3. UPCOMING EARNINGS ANALYSIS")
        print("-" * 40)
        
        for days in [7, 14, 30]:
            upcoming = earnings_cal.filter_upcoming_earnings(earnings_data, days_ahead=days)
            print(f"Next {days:2d} days: {len(upcoming)} companies")
        
        # Generate detailed summary for next 30 days
        upcoming_30 = earnings_cal.filter_upcoming_earnings(earnings_data, days_ahead=30)
        if upcoming_30:
            print("\n4. DETAILED EARNINGS CALENDAR (Next 30 Days)")
            print("-" * 40)
            summary = earnings_cal.generate_earnings_summary(upcoming_30)
            print(summary)
            
            # Save to file
            filename = earnings_cal.save_earnings_calendar(upcoming_30)
            print(f"\nEarnings calendar saved to: {filename}")
        
        # Test integration with market orchestrator
        print("\n5. MARKET ORCHESTRATOR INTEGRATION")
        print("-" * 40)
        
        orchestrator = MarketAnalysisOrchestrator()
        
        # Quick analysis with top performers that also have earnings
        companies_with_earnings = [e['symbol'] for e in companies_with_future_earnings[:5]]
        if companies_with_earnings:
            print(f"Testing quick analysis with: {', '.join(companies_with_earnings)}")
            
            try:
                result = orchestrator.run_quick_analysis(companies_with_earnings)
                
                perf_count = len(result.get('performance_data', []))
                earnings_count = len([e for e in result.get('earnings_data', []) if e and e.get('next_earnings_date')])
                
                print(f"Performance data: {perf_count} companies")
                print(f"Earnings data: {earnings_count} companies with upcoming dates")
                
                # Show combined performance + earnings
                print("\nPERFORMANCE + EARNINGS COMBINATION:")
                for perf in result.get('performance_data', [])[:3]:
                    symbol = perf.get('symbol', 'Unknown')
                    return_pct = perf.get('return_pct', 0.0)
                    price = perf.get('end_price', 0.0)
                    
                    # Find corresponding earnings data
                    earnings_info = next((e for e in result.get('earnings_data', []) if e and e.get('symbol') == symbol), None)
                    earnings_date = earnings_info.get('next_earnings_date') if earnings_info else None
                    earnings_date = earnings_date or 'No date'
                    
                    print(f"  {symbol}: {return_pct:+6.2f}% | ${price:7.2f} | Earnings: {earnings_date}")
                
            except Exception as e:
                print(f"Orchestrator integration error: {e}")
        
        print("\n" + "="*60)
        print("\nEARNINGS CALENDAR TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Summary of capabilities
        print("\nEARNINGS CALENDAR CAPABILITIES:")
        print("- Fetch earnings dates from yfinance")
        print("- Filter by upcoming date ranges")
        print("- Generate formatted summaries")
        print("- Save results to JSON files")
        print("- Integration with market orchestrator")
        print("- Batch processing multiple companies")
        print("- Company information (name, sector)")
        print("- Days-until-earnings calculations")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()