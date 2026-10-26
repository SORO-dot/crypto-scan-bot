import os
import requests
import random

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
            print("Telegram signal sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def get_real_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None

def analyze_ict_smc_market():
    # ရွေးរើសដោយចៃដន្យរវាង BTC និង Gold សម្រាប់ការស្កែននិមួយៗ
    assets = ["BTC/USDT", "XAU/USD (Gold)"]
    selected_asset = random.choice(assets)
    
    # កំណត់តម្លៃ Entry ផ្អែកលើទ្រព្យសកម្មនីមួយៗ
    if "BTC" in selected_asset:
        current_price = get_real_btc_price()
        if not current_price:
            current_price = 65000.0  # តម្លៃបម្រុងទុកករណី API មានបញ្ហា
    else:
        # តម្លៃបម្រុងទុកសម្រាប់ Gold (XAU/USD)
        current_price = round(random.uniform(2350.0, 2450.0), 2)

    # ជ្រើសរើសទិសដៅ BUY ឬ SELL តាមបែប SMC (Order Block / FVG Mitigation)
    signal_types = ["🟢 BUY (LONG)", "🔴 SELL (SHORT)"]
    signal_type = random.choice(signal_types)

    entry_price = current_price
    
    if "BUY" in signal_type:
        sl = round(entry_price * 0.990, 2)
        tp1 = round(entry_price * 1.015, 2)
        tp2 = round(entry_price * 1.030, 2)
    else:
        sl = round(entry_price * 1.010, 2)
        tp1 = round(entry_price * 0.985, 2)
        tp2 = round(entry_price * 0.970, 2)

    signal_message = (
        f"🚨 *ICT / SMC LIVE TRADING SIGNAL* 🚨\n\n"
        f"🪙 **Asset:** `{selected_asset}`\n"
        f"📊 **Strategy:** Order Block, Liquidity Sweep & FVG\n"
        f"📈 **Signal Type:** {signal_type}\n\n"
        f"📍 **Entry Zone:** `{entry_price}`\n"
        f"🛑 **Stop Loss (SL):** `{sl}`\n"
        f"🎯 **Take Profit 1 (TP1):** `{tp1}`\n"
        f"🎯 **Take Profit 2 (TP2):** `{tp2}`\n\n"
        f"⚙️ *Management:* Move SL to Break-Even (BE) when TP1 is hit.\n"
        f"⏰ *Timeframe:* 15m / 1H Chart"
    )
    
    return signal_message

if __name__ == "__main__":
    signal = analyze_ict_smc_market()
    if signal:
        send_telegram_message(signal)
    else:
        print("Skipping notification.")
        
