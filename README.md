# Market Analysis System

A comprehensive Python system to track S&P 500 top performers, monitor earnings calendars, perform sentiment analysis, and send notifications via Telegram.

## 🚀 Features

- **S&P 500 Top Performers Tracking**: Analyzes all S&P 500 companies and ranks them by various performance metrics
- **Earnings Calendar**: Fetches quarterly earnings dates for companies using multiple financial APIs
- **Telegram Notifications**: Sends formatted market updates and alerts via Telegram bot
- **Sentiment Analysis**: Analyzes news sentiment for top performing companies
- **Complete Workflow**: Main orchestrator that combines all modules for automated analysis

## 📁 Project Structure

```
Share_market/
├── sp500_tracker.py          # S&P 500 performance analysis
├── earnings_calendar.py      # Earnings dates fetcher
├── telegram_bot.py          # Telegram notifications
├── sentiment_analyzer.py    # News sentiment analysis
├── market_orchestrator.py   # Main workflow orchestrator
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Installation

1. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (optional but recommended):
   - **Alpha Vantage**: Get free API key from https://www.alphavantage.co/support/#api-key
   - **News API**: Get free API key from https://newsapi.org/register
   - **Telegram Bot**: Create bot via @BotFather and get your chat ID

3. **Configure the system**:
   ```bash
   python market_orchestrator.py --setup
   ```

## 🚀 Usage

### Quick Start
Run complete analysis with default settings:
```bash
python market_orchestrator.py
```

### Advanced Usage

**Analyze by different metrics**:
```bash
python market_orchestrator.py --metric return_pct    # By price returns
python market_orchestrator.py --metric volume_ratio  # By volume activity  
python market_orchestrator.py --metric volatility    # By price volatility
```

**Skip Telegram notifications**:
```bash
python market_orchestrator.py --no-telegram
```

**Quick analysis for specific stocks**:
```bash
python market_orchestrator.py --quick AAPL MSFT GOOGL
```

### Individual Modules

**S&P 500 Tracker**:
```python
from sp500_tracker import SP500Tracker

tracker = SP500Tracker()
top_performers = tracker.get_top_performers(metric='return_pct', top_n=20)
print(tracker.get_performance_summary(top_performers, 'return_pct'))
```

**Earnings Calendar**:
```python
from earnings_calendar import EarningsCalendar

calendar = EarningsCalendar()
earnings = calendar.get_company_earnings_info(['AAPL', 'MSFT', 'GOOGL'])
upcoming = calendar.filter_upcoming_earnings(earnings, days_ahead=30)
```

**Sentiment Analysis**:
```python
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze_company_sentiment('AAPL', 'Apple Inc.')
print(f"Sentiment: {sentiment['overall_sentiment']} (Score: {sentiment['overall_score']:.2f})")
```

**Telegram Bot**:
```python
from telegram_bot import TelegramBot

bot = TelegramBot('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')
bot.send_market_update(top_performers=performers_data, earnings_data=earnings_data)
```

## 🔧 Configuration

The system uses a `market_config.json` file for configuration. Run setup to create it:

```bash
python market_orchestrator.py --setup
```

Example configuration:
```json
{
  "alpha_vantage_key": "YOUR_ALPHA_VANTAGE_KEY",
  "news_api_key": "YOUR_NEWS_API_KEY", 
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID",
  "analysis_settings": {
    "top_performers_count": 15,
    "performance_period": "1mo",
    "earnings_days_ahead": 30,
    "sentiment_days_back": 7,
    "min_market_cap": 1000000000
  }
}
```

## 📱 Setting up Telegram Bot

1. **Create a bot**:
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Get your Chat ID**:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Test the connection**:
   ```python
   from telegram_bot import TelegramBot
   bot = TelegramBot('YOUR_TOKEN', 'YOUR_CHAT_ID')
   bot.test_connection()
   ```

## 📊 Output Files

The system generates several output files:

- `top_performers_*.json` - Top performing companies data
- `earnings_calendar_*.json` - Earnings calendar data  
- `sentiment_analysis_*.json` - Sentiment analysis results
- `market_analysis_complete_*.json` - Complete workflow results

## 🔄 Automation

To run automatically, you can:

1. **Use Windows Task Scheduler**:
   - Create a task to run the Python script daily
   - Set trigger for market hours (e.g., 9:30 AM ET)

2. **Use cron (Linux/Mac)**:
   ```bash
   # Run daily at 9:30 AM
   30 9 * * 1-5 cd /path/to/project && python market_orchestrator.py
   ```

3. **Python scheduler**:
   ```python
   import schedule
   import time
   
   def run_analysis():
       from market_orchestrator import MarketAnalysisOrchestrator
       orchestrator = MarketAnalysisOrchestrator()
       orchestrator.run_full_analysis()
   
   schedule.every().day.at("09:30").do(run_analysis)
   
   while True:
       schedule.run_pending()
       time.sleep(60)
   ```

## ⚠️ Important Notes

- **Rate Limits**: The system includes delays to respect API rate limits
- **Free APIs**: Many features work with free APIs, but paid APIs provide more data
- **Market Hours**: Best results during market hours (9:30 AM - 4:00 PM ET)
- **Data Accuracy**: Financial data is for informational purposes only

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for educational and personal use. Please respect API terms of service and rate limits.

---

**Disclaimer**: This tool is for informational purposes only and should not be considered as financial advice. Always do your own research before making investment decisions.