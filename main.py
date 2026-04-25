import telebot
import requests
import threading
import time
from flask import Flask

# --- কনফিগারেশন ---
TELEGRAM_TOKEN = "8683108194:AAFevIXVBrWPKvWQAs2KAjIh9ZTWa3O2M2Q"
GROQ_API_KEY = "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"
USER_CHAT_ID = "8305902471"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Nexus Alpha is Alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def get_signal():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = "Provide a Gold (XAUUSD) BUY/SELL signal in BENGALI with Entry, TP, SL and analysis."
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    try:
        # আমরা Timeout বাড়িয়ে ৩০ সেকেন্ড করলাম যাতে AI ভাবার সময় পায়
        r = requests.post(url, headers=headers, json=data, timeout=30)
        res = r.json()
        if 'choices' in res:
            return res['choices'][0]['message']['content']
        return "⚠️ AI Response Error: " + str(res.get('error', {}).get('message', 'Unknown'))
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

def auto_loop():
    # প্রথম স্টার্ট মেসেজ
    bot.send_message(USER_CHAT_ID, "🛠️ **System Hard-Reset Done!**\nঅটোমেশন ইঞ্জিন এখন প্রতি ১০ মিনিট পর পর জোরপূর্বক সিগন্যাল জেনারেট করবে।")
    
    while True:
        print("Scraping for signal...")
        signal = get_signal()
        
        if signal:
            bot.send_message(USER_CHAT_ID, signal)
            print("Message delivered.")
        else:
            # যদি সিগন্যাল না আসে তবে আপনাকে জানাবে কেন আসছে না
            bot.send_message(USER_CHAT_ID, "🔍 মার্কেট স্ক্যান করা হয়েছে কিন্তু এআই থেকে ডাটা পাওয়া যায়নি। ১০ মিনিট পর আবার চেষ্টা হবে।")

        # ১০ মিনিট বিরতি (৬০০ সেকেন্ড)
        time.sleep(600)

if __name__ == "__main__":
    # ওয়েব সার্ভার আলাদা থ্রেডে
    threading.Thread(target=run_web_server).start()
    
    # অটোমেশন আলাদা থ্রেডে
    threading.Thread(target=auto_loop).start()
    
    # মেইন বডি হিসেবে পোলিং
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
