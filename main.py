import telebot
import requests
import threading
import time
from flask import Flask

# --- আপনার সঠিক কনফিগারেশন ---
TELEGRAM_TOKEN = "8496380165:AAFJShJPVYlP9UDpX1LVtLwHUE9PwAOKv1U"
GROQ_API_KEY = "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"
USER_CHAT_ID = "8305902471"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Nexus Alpha is Alive and Running!"

def run_web_server():
    # Render-এর জন্য এই পোর্টটি দরকার
    app.run(host='0.0.0.0', port=8080)

def get_signal():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = """
    You are an expert XAUUSD (Gold) trader. Provide a high-conviction BUY or SELL signal in BENGALI.
    Format:
    🔱 **NEXUS CLOUD SNIPER** 🔱
    ━━━━━━━━━━━━━━━━━━
    📈 Action: [BUY or SELL]
    📍 Entry: [Price]
    🎯 TP: [Price] | 🛡️ SL: [Price]
    📊 Analysis: [Reason in Bengali]
    ━━━━━━━━━━━━━━━━━━
    """
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=25)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def auto_loop():
    # রান করার সাথে সাথেই একটি মেসেজ যাবে যাতে আপনি কনফার্ম হতে পারেন
    try:
        bot.send_message(USER_CHAT_ID, "✅ **Cloud Connection Successful!**\nআপনার বটটি এখন Render সার্ভার থেকে ২৪/৭ সচল। প্রতি ১৫ মিনিট পর পর আপডেট আসবে।")
    except:
        pass

    while True:
        signal = get_signal()
        if signal:
            try:
                bot.send_message(USER_CHAT_ID, signal)
                print("Signal Sent Successfully!")
            except Exception as e:
                print(f"Telegram Error: {e}")
        
        # ১৫ মিনিট (১০০ সেকেন্ড) বিরতি
        time.sleep(100)

if __name__ == "__main__":
    # ওয়েব সার্ভার চালু করা (Render-কে শান্ত রাখার জন্য)
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # অটোমেশন লুপ চালু করা
    threading.Thread(target=auto_loop, daemon=True).start()
    
    # বট পোলিং
    print("Bot is starting on Cloud...")
    bot.polling(none_stop=True)
