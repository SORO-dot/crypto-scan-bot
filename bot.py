import os
import requests

# ទាញយក Token និង Chat ID ពី GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing!")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # សារសាកល្បងផ្ញើចូល Telegram ដើម្បីเช็คការតភ្ជាប់
    test_message = "🤖 *ICT/SMC Trading Bot* ត្រូវបានភ្ជាប់ដោយជោគជ័យ!\n\n📈 កំពុងត្រៀមស្កែនទីផ្សារ BTC និង Gold 24/7..."
    send_telegram_message(test_message)
    
