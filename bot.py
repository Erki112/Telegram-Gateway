import telebot
import requests
import time
import threading

# --- ODEEFFANNOO KEE ---
TOKEN = "8783344805:AAF7Jky-d_sRfD7Tw_cVvLPRjAHPApCs2eM"
MY_CHAT_ID = 6097824995 
SERVEO_URL = "https://74be83e565fc4686-196-189-182-71.serveousercontent.com"

bot = telebot.TeleBot(TOKEN)
last_otp_time = ""

def monitor_sms():
    global last_otp_time
    print("🕵️ Hordoffii SMS battalaa jalqabeera...")
    while True:
        try:
            # Timeout itti daballee akka inni hin dhaabbanne gochuuf
            response = requests.get(f"{SERVEO_URL}/get_otp", timeout=30)
            if response.status_code == 200:
                res = response.json()
                if "otp_message" in res:
                    current_time = res.get('time', str(time.time()))
                    if current_time != last_otp_time:
                        last_otp_time = current_time
                        notification = (
                            f"🔔 **SMS HAARAA DHUFE!**\n\n"
                            f"💬 {res['otp_message']}\n"
                            f"👤 **Irraayi:** {res.get('from', 'Unknown')}"
                        )
                        bot.send_message(MY_CHAT_ID, notification)
        except Exception as e:
            print(f"⚠️ Connection eegamaa jira... (Server Offline ta'uu danda'a)")
        time.sleep(10)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id != MY_CHAT_ID: return
    welcome_text = "🚀 **Gateway Nekemte 'Online' dha!**"
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['status'])
def check_status(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        res = requests.get(f"{SERVEO_URL}/get_otp", timeout=15)
        if res.status_code == 200:
            bot.send_message(message.chat.id, "✅ Server kee Nekemte irratti 'Live' dha!")
        else:
            bot.send_message(message.chat.id, f"⚠️ Server ni deebisa garuu rakkoon jira: {res.status_code}")
    except:
        bot.send_message(message.chat.id, "❌ Server 'Offline' dha. Serveo/Termux mirkaneessi.")

# Threading jalqabuu
threading.Thread(target=monitor_sms, daemon=True).start()

print("🚀 Bot kee hojii jalqabeera...")
# none_stop=True akka inni dogoggoraan hin dhaabbanne godha
bot.polling(none_stop=True, timeout=60)

