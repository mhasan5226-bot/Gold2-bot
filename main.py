import telebot
import requests
import threading
import time
from flask import Flask

# --- নতুন কনফিগারেশন ---
TELEGRAM_TOKEN = "8683108194:AAFevIXVBrWPKvWQAs2KAjIh9ZTWa3O2M2Q"
GROQ_API_KEY = "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"
USER_CHAT_ID = "8305902471"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Nexus Alpha Stable Mode Active!"

def run_web_server():
    # Render এর জন্য পোর্ট ৮MD০৮০ ফিক্সড রাখা হয়েছে
    app.run(host='0.0.0.0', port=8080)

def get_signal():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # ইনজেকশন করা প্রম্পট যা সরাসরি সিগন্যাল দিতে বাধ্য করবে
    prompt = """
    Act as a professional Gold (XAUUSD) technical analyst. 
    Analyze market trends and provide a clear BUY/SELL signal in BENGALI.
    
    Format:
    🔱 **NEXUS MASTER SNIPER** 🔱
    ━━━━━━━━━━━━━━━━━━
    📈 Action: [BUY or SELL]
    📍 Entry: [Current Market Price]
    🎯 TP: [Target Profit]
    🛡️ SL: [Stop Loss]
    
    📊 Analysis: [2-line technical reason in Bengali]
    ━━━━━━━━━━━━━━━━━━
    """
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        res_json = response.json()
        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"AI Fetch Error: {e}")
        return None

def auto_loop():
    # নতুন বটের প্রথম মেসেজ
    try:
        bot.send_message(USER_CHAT_ID, "🚀 **New Bot Connected Successfully!**\nআপনার নতুন বটটি এখন Render ক্লাউড থেকে সরাসরি নিয়ন্ত্রিত। প্রতি ১০ মিনিট পর পর অটোমেটিক সিগন্যাল আসবে।")
    except Exception as e:
        print(f"Welcome Message Error: {e}")

    while True:
        print("Checking Market...")
        signal = get_signal()
        
        if signal:
            try:
                bot.send_message(USER_CHAT_ID, signal)
                print("Signal Sent!")
            except Exception as e:
                print(f"Telegram Delivery Error: {e}")
        
        # ১০ মিনিট বিরতি (৬০০ সেকেন্ড)
        time.sleep(600)

if __name__ == "__main__":
    # ওয়েব সার্ভার ব্যাকগ্রাউন্ডে রাখা
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # অটোমেশন লুপ ব্যাকগ্রাউন্ডে রাখা
    threading.Thread(target=auto_loop, daemon=True).start()
    
    # বট পোলিং (এরর হ্যান্ডলিং সহ)
    while True:
        try:
            print("Bot Polling Started...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Polling Restarting due to: {e}")
            time.sleep(10)
