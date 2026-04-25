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
    return "Nexus Alpha 2.0 is Alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def get_signal():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # আমরা মডেল আপডেট করে llama3-70b-8192 দিচ্ছি যা অনেক শক্তিশালী
    data = {
        "model": "llama3-70b-8192", 
        "messages": [{"role": "user", "content": "Provide a high-quality Gold (XAUUSD) trading signal in BENGALI. Action, Entry, TP, SL and analysis."}],
        "temperature": 0.6
    }
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        res = r.json()
        if 'choices' in res:
            return res['choices'][0]['message']['content']
        return f"⚠️ AI Error: {res.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

def auto_loop():
    # প্রথম স্টার্ট মেসেজ
    bot.send_message(USER_CHAT_ID, "✅ **Model Updated to Llama3-70B!**\nএখন থেকে এআই নিয়মিত সিগন্যাল দিতে পারবে। প্রতি ১০ মিনিট পর পর চেক করা হবে।")
    
    while True:
        print("Checking for signal...")
        signal = get_signal()
        
        if signal:
            bot.send_message(USER_CHAT_ID, signal)
            print("Signal Sent.")
        
        time.sleep(600) # ১০ মিনিট

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    threading.Thread(target=auto_loop).start()
    
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            time.sleep(10)
