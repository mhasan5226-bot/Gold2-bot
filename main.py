import telebot
import requests
import threading
import time
from flask import Flask

# --- কনফিগারেশন ---
TELEGRAM_TOKEN = "8496380165:AAFJShJPVYlP9UDpX1LVtLwHUE9PwAOKv1U"
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
    prompt = "Provide a Gold (XAUUSD) signal in BENGALI with Action, Entry, TP, SL."
    data = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except: return None

def auto_loop():
    while True:
        signal = get_signal()
        if signal:
            bot.send_message(USER_CHAT_ID, "🚀 **CLOUD SIGNAL**\n\n" + signal)
        time.sleep(900) # ১৫ মিনিট পর পর

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    threading.Thread(target=auto_loop).start()
    bot.polling(none_stop=True)
