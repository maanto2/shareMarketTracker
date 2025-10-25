# Configuration Setup Guide

## Quick Setup

1. **Copy the example environment file:**
   ```bash
   # On Windows
   copy .env.example .env
   
   # On Linux/Mac
   cp .env.example .env
   ```

2. **Edit the `.env` file with your personal details:**
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   TELEGRAM_CHAT_ID=your_actual_chat_id_here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the system:**
   ```bash
   python start_news_monitor.py
   ```

## Configuration Files

### `.env` (Personal - Not uploaded to Git)
Contains your personal Telegram credentials:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: Your personal chat ID
- `NEWS_API_KEY`: (Optional) Your NewsAPI key
- `ALPHA_VANTAGE_KEY`: (Optional) Your Alpha Vantage key

### `news_monitor_config.json` (Public - Safe to upload)
Contains system configuration:
- Monitoring settings (symbols, intervals, keywords)
- Alert preferences
- Filtering options
- Placeholder values for sensitive data

## Getting Your Telegram Credentials

### Bot Token
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token to your `.env` file

### Chat ID
1. Start a conversation with your bot
2. Run: `python get_chat_id.py`
3. Copy the chat ID to your `.env` file

## Security Notes

- The `.env` file is automatically excluded from Git commits
- Never commit real tokens or chat IDs to version control
- The public config file uses placeholder values
- Personal earnings data files are also excluded from Git

## Testing

Test your configuration:
```bash
python config_loader.py
```

This should show:
```
Configuration loaded successfully!
Bot token present: Yes
Chat ID present: Yes
```