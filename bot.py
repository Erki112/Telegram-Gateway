import telebot
import requests

TOKEN = "8783344805:AAF7Jky-d_sRfD7Tw_cVvLPRjAHPApCs2eM"
bot = telebot.TeleBot(TOKEN)

# Gateway Codespaces keessa jiru (Local)
GATEWAY_URL = "http://127.0.0.1:5000"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 **Bot kee GitHub irratti 'Live' dha!**\n\n/status - Mirkaneessuuf\n/call [num] - Bilbila eegaluuf\n/getotp - SMS dubbisuuf")

@bot.message_handler(commands=['status'])
def check_status(message):
    try:
        res = requests.get(f"{GATEWAY_URL}/get_latest", timeout=5)
        if res.status_code == 200:
            bot.reply_to(message, "✅ **Gateway Nekemte 'Online' dha!**")
    except:
        bot.reply_to(message, "❌ **Gateway 'Offline' dha.** Termux ykn Codespaces mirkaneessi.")

@bot.message_handler(commands=['call'])
def start_call(message):
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ Fakkeenya: `/call 09...` galchi.")
    
    number = args[1]
    bot.reply_to(message, f"📞 Bilbilli gara {number} eegalameera... OTP eegaa jirra.")
    # Asirratti Gateway kee 'Trigger' gochuu dandeessa

@bot.message_handler(commands=['getotp'])
def get_otp(message):
    try:
        data = requests.get(f"{GATEWAY_URL}/get_latest").json()
        bot.reply_to(message, f"📩 **SMS Dhuma Dhufe:**\n\n{data['body']}\n\nIrraa: {data['from']}")
    except:
        bot.reply_to(message, "❌ Koodii argachuu hin dandeenye.")

bot.infinity_polling()
