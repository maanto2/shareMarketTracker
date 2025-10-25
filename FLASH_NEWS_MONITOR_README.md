# Flash News Monitor - Documentation

## Overview
The Flash News Monitor is an automated system that watches for breaking news affecting the stock market and sends real-time Telegram alerts when important events occur.

## Features

### 🔍 **News Sources**
- Yahoo Finance RSS feeds (S&P 500, NASDAQ, Dow Jones)
- NewsAPI integration (optional - requires API key)
- Real-time monitoring of market-moving events

### 📊 **Smart Stock Detection**
- Automatically detects mentioned stock symbols in news
- Monitors 30+ major stocks by default (AAPL, MSFT, GOOGL, etc.)
- Easily customizable symbol list

### ⚡ **Intelligent Urgency Scoring**
- Assigns urgency scores (1-10) based on content analysis
- High-priority keywords: earnings, mergers, FDA approvals, etc.
- Market-wide impact detection: Fed announcements, interest rates, etc.

### 📱 **Telegram Integration**
- Instant notifications to your phone
- HTML-formatted messages with urgency indicators
- Rate limiting to prevent spam

## Files

### Core Files
- `flash_news_monitor.py` - Main monitoring system
- `start_news_monitor.py` - Simple startup script
- `news_monitor_config.json` - Configuration settings

### Setup Files
- `telegram_connection_test.py` - Test Telegram bot connection
- `get_chat_id.py` - Helper to find your Telegram chat ID

## Quick Start

### 1. Test the System
```bash
python flash_news_monitor.py
# Choose option 1 to test alerts
```

### 2. Start Monitoring
```bash
python start_news_monitor.py
# Starts monitoring with default 5-minute intervals
```

### 3. Manual Control
```bash
python flash_news_monitor.py
# Choose option 2 for normal monitoring (5 min)
# Choose option 3 for high-frequency monitoring (1 min)
```

## Configuration

### Telegram Settings
- `bot_token` - Your Telegram bot token from @BotFather
- `chat_id` - Your personal Telegram user ID

### Monitoring Settings
- `check_interval_minutes` - How often to check for news (default: 5)
- `symbols_to_monitor` - List of stock symbols to watch
- `minimum_urgency_score` - Minimum score needed to send alert (default: 3)

### Alert Examples

#### High Urgency (Score 8-10)
```
[URGENT] MARKET NEWS ALERT

Symbols: AAPL
Urgency: 9/10

Federal Reserve Announces Emergency Interest Rate Cut

The Federal Reserve announced an unexpected 0.5% 
interest rate cut in response to market volatility...

Source: Yahoo Finance RSS
Time: 14:30:15
Keywords: federal reserve, interest rates
```

#### Medium Urgency (Score 4-7)
```
[MEDIUM] MARKET NEWS ALERT

Symbols: AAPL
Urgency: 6/10

Apple Reports Record Q4 Earnings, Beats Expectations

Apple Inc. reported quarterly earnings that exceeded 
analyst expectations...

Source: Yahoo Finance RSS
Time: 14:30:15
Keywords: earnings beat
```

## Monitored Keywords

### High Impact Keywords
- Earnings (beat, miss, guidance)
- Corporate actions (merger, acquisition, split)
- Regulatory (FDA approval, recall, lawsuit)
- Leadership (CEO changes, layoffs)
- Market events (crash, correction, halt)

### Market-Wide Keywords
- Federal Reserve, interest rates
- Inflation, recession, GDP
- Oil prices, cryptocurrency
- Market indices (S&P 500, NASDAQ, Dow)

## Default Monitored Stocks

### Tech Giants
AAPL, MSFT, GOOGL, AMZN, META, NVDA

### Financial & Healthcare  
JPM, V, MA, UNH, JNJ, PFE

### Consumer & Industrial
WMT, HD, DIS, KO, PEP, PG

### ETFs & Indices
SPY, QQQ, IWM, VIX

## Usage Tips

### 1. Start with Normal Monitoring
Begin with 5-minute intervals to avoid overwhelming notifications.

### 2. Customize Symbol List
Edit `news_monitor_config.json` to add/remove stocks you care about.

### 3. Adjust Urgency Threshold
Increase `minimum_urgency_score` if getting too many alerts.

### 4. Market Hours vs 24/7
- Set `only_market_hours: true` for trading hours only
- Keep `false` for after-hours and weekend news

### 5. Rate Limiting
The system prevents spam by:
- Tracking sent alerts to avoid duplicates
- Rate limiting (max 10 alerts per hour)
- 2-second delays between messages

## Running Continuously

### Option 1: Keep Terminal Open
```bash
python start_news_monitor.py
# Keep the terminal window open
```

### Option 2: Background Process (Advanced)
```bash
# Windows - run in background
python start_news_monitor.py &

# Or use Task Scheduler for automatic startup
```

## Troubleshooting

### Common Issues

#### "Chat not found" Error
- Check your chat ID is correct
- Make sure you've messaged your bot first

#### "Bot token invalid" Error  
- Verify token from @BotFather
- Check format: numbers:letters (e.g., 123456:ABCdef)

#### No Alerts Received
- Run single news check (option 4) to test
- Lower `minimum_urgency_score` in config
- Check if symbols are mentioned in current news

#### Too Many Alerts
- Increase `minimum_urgency_score`
- Reduce monitored symbols
- Increase check interval

### Getting Support
- Test individual components first
- Check Telegram bot with `telegram_connection_test.py`
- Verify news sources are accessible
- Review console output for error messages

## Advanced Features

### Custom Keywords
Add your own keywords to the config file:
```json
"urgent_keywords": [
  "your custom keyword",
  "another important term"
]
```

### NewsAPI Integration
Get a free API key from newsapi.org for more comprehensive news coverage:
```json
"news_apis": {
  "news_api_key": "your_newsapi_key_here"
}
```

### Symbol Groups
Create different monitoring profiles:
- Tech stocks only
- Financial sector focus  
- Crypto-related stocks
- Market indices only

The Flash News Monitor provides real-time market intelligence directly to your phone, helping you stay informed about events that could impact your investments!