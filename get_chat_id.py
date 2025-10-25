"""
Get Chat ID Helper
This script helps you find your Telegram chat ID
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

def get_chat_id_from_bot(bot_token):
    """Get chat ID by having someone message your bot"""
    print("FINDING YOUR CHAT ID")
    print("=" * 30)
    
    print("Steps to get your Chat ID:")
    print("1. Go to Telegram")
    print("2. Search for your bot (the one you created with @BotFather)")
    print("3. Send any message to your bot (like 'hello')")
    print("4. Come back here and press Enter")
    
    input("Press Enter after you've sent a message to your bot...")
    
    try:
        # Get updates from Telegram
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        data = response.json()
        
        if data['ok'] and data['result']:
            print(f"\nFound {len(data['result'])} message(s):")
            
            for update in data['result']:
                if 'message' in update:
                    chat = update['message']['chat']
                    chat_id = chat['id']
                    chat_type = chat['type']
                    
                    if chat_type == 'private':
                        first_name = chat.get('first_name', 'Unknown')
                        last_name = chat.get('last_name', '')
                        username = chat.get('username', 'No username')
                        
                        print(f"Chat ID: {chat_id}")
                        print(f"Name: {first_name} {last_name}")
                        print(f"Username: @{username}")
                        print(f"Type: {chat_type}")
                        
                        return str(chat_id)
            
            print("No private messages found. Make sure you sent a message to your bot!")
            
        else:
            print("No messages found. Make sure you:")
            print("1. Created the bot correctly")
            print("2. Sent a message to your bot")
            print("3. Used the correct bot token")
            
    except Exception as e:
        print(f"Error getting updates: {e}")
    
    return None

def main():
    # Use the token from your connection test file
    BOT_TOKEN = "8060365740:AAHBifQY747PaIfTjG39N2kdoLRUJXlDN9M"
    
    print("Getting your Chat ID...")
    print(f"Using bot token: {BOT_TOKEN[:10]}...")
    
    chat_id = get_chat_id_from_bot(BOT_TOKEN)
    
    if chat_id:
        print(f"\nSUCCESS! Your Chat ID is: {chat_id}")
        print(f"\nUpdate your telegram_connection_test.py file:")
        print(f'Change CHAT_ID = "@gottcam_bot"')
        print(f'To     CHAT_ID = "{chat_id}"')
        
        # Test sending a message with the found chat ID
        print(f"\nTesting message with Chat ID {chat_id}...")
        
        try:
            import sys
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from telegram_bot import TelegramBot
            
            bot = TelegramBot(BOT_TOKEN, chat_id)
            success = bot.send_message("🎉 Chat ID found! Your Telegram bot is working!")
            
            if success:
                print("SUCCESS: Test message sent to your Telegram!")
            else:
                print("Message sending failed, but Chat ID should still work")
                
        except Exception as e:
            print(f"Test message error: {e}")
    
    else:
        print("\nCould not find your Chat ID.")
        print("Make sure you:")
        print("1. Have sent a message to your bot")
        print("2. Are using the correct bot token")

if __name__ == "__main__":
    main()