#!/usr/bin/env python3
"""
Master Launch Script for Market Analysis System
Choose which system to run: unified, news-only, or analysis-only
"""

import sys
import os

def show_menu():
    """Display the main menu"""
    print("🚀 MARKET ANALYSIS SYSTEM LAUNCHER")
    print("=" * 50)
    print("Choose your system:")
    print()
    print("1. 🌟 UNIFIED SYSTEM (Recommended)")
    print("   - Real-time news alerts + Market analysis reports")
    print("   - Runs both systems in parallel")
    print("   - Complete market monitoring solution")
    print()
    print("2. 📰 NEWS MONITOR ONLY")
    print("   - Real-time breaking news alerts")
    print("   - Fast news notifications via Telegram")
    print()
    print("3. 📊 MARKET ANALYSIS ONLY")
    print("   - S&P 500 analysis + Earnings calendar + Sentiment")
    print("   - Comprehensive reports every 4 hours")
    print()
    print("4. 🧪 TEST SYSTEMS")
    print("   - Test alerts and configuration")
    print()
    print("5. ❌ EXIT")
    print()

def main():
    """Main launcher"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🌟 Starting UNIFIED SYSTEM...")
                print("This will run both real-time news monitoring AND market analysis in parallel")
                confirm = input("Continue? (y/n): ").strip().lower()
                if confirm == 'y':
                    os.system("python unified_market_system.py")
                
            elif choice == "2":
                print("\n📰 Starting NEWS MONITOR ONLY...")
                os.system("python start_news_monitor.py")
                
            elif choice == "3":
                print("\n📊 Starting MARKET ANALYSIS ONLY...")
                os.system("python market_orchestrator.py")
                
            elif choice == "4":
                print("\n🧪 TESTING OPTIONS:")
                print("1. Test news alerts")
                print("2. Test market analysis")
                print("3. Test Telegram connection")
                
                test_choice = input("Choose test (1-3): ").strip()
                if test_choice == "1":
                    os.system("python test_alert_direct.py")
                elif test_choice == "2":
                    os.system("python test_system.py")
                elif test_choice == "3":
                    os.system("python telegram_connection_test.py")
                
            elif choice == "5":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("\n❌ Invalid choice. Please select 1-5.")
                
            input("\nPress Enter to return to menu...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()