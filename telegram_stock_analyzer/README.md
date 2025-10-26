# Telegram Stock Analyzer

An interactive Telegram bot that provides real-time stock analysis and BUY/SELL recommendations.

## 🚀 Features

- **📊 Real-time Stock Analysis**: Get comprehensive analysis for any stock symbol
- **🎯 Smart Recommendations**: AI-powered BUY/SELL/HOLD predictions with confidence levels
- **📈 Technical Analysis**: RSI, moving averages, volume analysis, price momentum
- **📰 News Sentiment**: Analyzes recent news articles for sentiment scoring
- **💬 Interactive Bot**: Simple Telegram interface - just send a stock symbol
- **🔒 Secure**: Configurable authorized user list

## 📱 How to Use

1. **Send a stock symbol** to your bot (e.g., `AAPL`, `TSLA`, `MSFT`)
2. **Get instant analysis** with:
   - Current price and performance
   - Technical indicators
   - News sentiment analysis
   - BUY/SELL/HOLD recommendation
   - Confidence level and reasoning

## 🛠️ Setup Instructions

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token (looks like: `1234567890:ABCdefGhIjKlMnOpQrStUvWxYz`)

### 2. Get Your Chat ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send any message
3. Copy your chat ID (a number like: `123456789`)

### 3. Install Dependencies

```bash
pip install yfinance pandas numpy requests
```

### 4. Configure the Bot

Copy the template config file:

```bash
cp telegram_config.template.json telegram_config.json
```

Or run the main script to create the config file:

```bash
python main.py
```

Edit `telegram_config.json` with your details:

```json
{
  "bot_token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
  "authorized_chat_ids": ["YOUR_CHAT_ID_HERE"],
  "news_api_key": null
}
```

### 5. Start the Bot

```bash
python main.py
```

## 📊 Analysis Features

### Technical Analysis
- **Price Performance**: 1-day, 1-week, 1-month changes
- **RSI Indicator**: Identifies overbought/oversold conditions
- **Moving Averages**: 20-day and 50-day MA positioning
- **Volume Analysis**: Compares current vs average volume
- **Volatility Metrics**: Price volatility measurements

### Sentiment Analysis
- **News Collection**: Gathers recent news from multiple sources
- **Sentiment Scoring**: Analyzes positive/negative sentiment
- **Confidence Rating**: Reliability of sentiment analysis
- **Article Count**: Number of articles analyzed

### Smart Recommendations
- **Weighted Scoring**: Technical (60%) + Sentiment (30%) + Fundamental (10%)
- **Confidence Levels**: High/Medium/Low confidence ratings
- **Detailed Reasoning**: Explains why the recommendation was made
- **Risk Assessment**: Considers multiple factors for safety

## 🎯 Bot Commands

- **Stock Symbol** (e.g., `AAPL`) - Get full stock analysis
- `/help` - Show help message
- `/status` - Check bot status

## 📈 Example Output

```
📊 STOCK ANALYSIS: AAPL
Apple Inc.
💰 Current Price: $175.43

🎯 RECOMMENDATION
🟢 BUY
📈 Confidence: 78.5%
💡 Reason: Strong technical indicators align with positive news sentiment

📈 TECHNICAL ANALYSIS
🟢 1-Day: +2.30%
🟢 1-Week: +5.70%
🔴 1-Month: -1.20%
📈 Volume Ratio: 1.80x
📊 RSI: 65.0 ⚪ Neutral

📰 NEWS SENTIMENT
😊 Overall: POSITIVE
📊 Score: +2.10
📄 Articles: 6

🏢 COMPANY INFO
🏭 Sector: Technology
💰 Market Cap: $2.80T
📊 P/E Ratio: 25.40
```

## ⚙️ Configuration Options

### Optional NewsAPI Integration
For enhanced news analysis, get a free API key from [newsapi.org](https://newsapi.org):

```json
{
  "news_api_key": "your_newsapi_key_here"
}
```

### Multiple Users
Add multiple chat IDs to allow multiple users:

```json
{
  "authorized_chat_ids": ["123456789", "987654321", "555666777"]
}
```

## 🔧 Files Structure

```
telegram_stock_analyzer/
├── main.py                    # Main runner and configuration
├── interactive_telegram_bot.py # Telegram bot interface
├── stock_analyzer.py         # Stock analysis engine
├── prediction_engine.py      # BUY/SELL prediction logic
├── telegram_config.json      # Configuration file (created automatically)
└── README.md                 # This file
```

## ⚠️ Important Notes

- **Not Financial Advice**: This tool is for educational/informational purposes only
- **Rate Limits**: Yahoo Finance has rate limits; don't spam requests
- **Data Accuracy**: Stock data is sourced from Yahoo Finance
- **News Sources**: Uses free news sources unless NewsAPI key is provided

## 🛡️ Security

- **Authorized Users**: Only configured chat IDs can use the bot
- **Token Security**: Keep your bot token secure and never share it
- **Private Chats**: Bot works in private chats only for security

## 🚀 Getting Started

1. Clone/download the files
2. Run `python main.py` to create config
3. Edit `telegram_config.json` with your bot token and chat ID  
4. Run `python main.py` again to start the bot
5. Message your bot with any stock symbol!

## 📞 Support

If you encounter issues:

1. Check your bot token and chat ID are correct
2. Ensure all dependencies are installed
3. Verify your internet connection
4. Check that your bot has proper permissions

Happy trading! 📈🚀