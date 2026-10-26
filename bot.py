import os
import json
import urllib.request
import urllib.parse

# យកតម្លៃពី GitHub Secrets ដោយសុវត្ថិភាព
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
STATE_FILE = "trade_state.json"

def send_telegram_message(text):
    if not TOKEN or not CHAT_ID:
        print("Error: Token or Chat ID not found!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error: {e}")

def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return float(data['price'])
    except Exception as e:
        print(f"API Error for {symbol}: {e}")
        return None

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def main():
    state = load_state()
    
    btc_price = get_price("BTCUSDT")
    gold_price = get_price("PAXGUSDT")
    
    symbols_data = {
        "BTCUSDT": btc_price,
        "GOLD": gold_price
    }
    
    for asset, current_price in symbols_data.items():
        if current_price is None:
            continue
            
        if asset not in state:
            tp = current_price * 1.008
            sl = current_price * 0.996
            be_target = current_price * 1.004
            
            state[asset] = {
                "entry": current_price,
                "tp": tp,
                "sl": sl,
                "be_target": be_target,
                "be_moved": False
            }
            
            msg = f"""🚀 **SMC / ICT SIGNAL SETUP** 🚀
━━━━━━━━━━━━━━━━━━
📊 **Asset:** {asset}
📌 **Action:** BUY (Order Block / BOS) 🟢
💰 **Entry:** ${current_price:,.2f}
🎯 **TP:** ${tp:,.2f} (+0.8%)
🛑 **SL:** ${sl:,.2f} (-0.4%)
━━━━━━━━━━━━━━━━━━"""
            send_telegram_message(msg)
            
        else:
            trade = state[asset]
            entry = trade["entry"]
            tp = trade["tp"]
            sl = trade["sl"]
            be_target = trade["be_target"]
            
            if current_price <= sl:
                msg = f"""❌ **STOP LOSS HIT** ❌
━━━━━━━━━━━━━━━━━━
📊 **Asset:** {asset}
💰 **Entry:** ${entry:,.2f}
🛑 **Hit SL:** ${current_price:,.2f} (-0.4%)
━━━━━━━━━━━━━━━━━━"""
                send_telegram_message(msg)
                del state[asset]
                
            elif current_price >= tp:
                msg = f"""🎯 **TAKE PROFIT HIT!** 🎯
━━━━━━━━━━━━━━━━━━
📊 **Asset:** {asset}
💰 **Entry:** ${entry:,.2f}
🎯 **Hit TP:** ${current_price:,.2f} (+0.8%)
✨ *Profit Secured!* ✨
━━━━━━━━━━━━━━━━━━"""
                send_telegram_message(msg)
                del state[asset]
                
            elif not trade["be_moved"] and current_price >= be_target:
                trade["be_moved"] = True
                msg = f"""🛡️ **MOVE TO BREAK-EVEN (BE)** 🛡️
━━━━━━━━━━━━━━━━━━
📊 **Asset:** {asset}
💰 **Entry:** ${entry:,.2f}
📍 **Current Price:** ${current_price:,.2f}
👉 *តម្លៃបានរត់មកពាក់កណ្តាលทางហើយ សូមរំកិល Stop Loss មក Entry (BE)!*
━━━━━━━━━━━━━━━━━━"""
                send_telegram_message(msg)

    save_state(state)

if __name__ == "__main__":
    main()
        
