import random
import telebot
from telebot import types

# ==============================
# التوكن حق البوت
# ==============================
BOT_TOKEN = "8914644995:AAEsH5-EkQ3fJhembj5NAlLaCxzXWnfQvzk"

bot = telebot.TeleBot(BOT_TOKEN)

PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD", "ETH/USD",
    "XAU/USD", "USD/CAD", "AUD/USD", "USD/CHF", "NZD/USD"
]

ACTIONS = ["شراء 🟢", "بيع 🔴"]


def generate_signal() -> str:
    pair = random.choice(PAIRS)
    action = random.choice(ACTIONS)
    confidence = random.randint(60, 95)
    entry = round(random.uniform(0.9, 2.5), 4)
    tp = round(entry * random.uniform(1.005, 1.02), 4)
    sl = round(entry * random.uniform(0.98, 0.995), 4)

    text = (
        f"📊 صفقة عشوائية جديدة\n\n"
        f"الزوج: {pair}\n"
        f"التوصية: {action}\n"
        f"نسبة الثقة: {confidence}%\n"
        f"سعر الدخول: {entry}\n"
        f"الهدف (TP): {tp}\n"
        f"وقف الخسارة (SL): {sl}\n\n"
        f"⚠️ هذه صفقة عشوائية تجريبية فقط ولا تمثل نصيحة استثمارية حقيقية."
    )
    return text


def signal_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 صفقة جديدة", callback_data="new_signal"))
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "أهلاً 👋\nاستخدم /signal للحصول على صفقة عشوائية (شراء أو بيع)."
    )


@bot.message_handler(commands=["signal"])
def signal_command(message):
    bot.send_message(
        message.chat.id,
        generate_signal(),
        reply_markup=signal_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == "new_signal")
def new_signal_callback(call):
    bot.edit_message_text(
        generate_signal(),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=signal_keyboard()
    )
    bot.answer_callback_query(call.id)


import time

print("البوت شغال...")

while True:
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=30)
    except Exception as e:
        print("صار انقطاع بالاتصال، جاري إعادة المحاولة بعد 5 ثواني...")
        print(e)
        time.sleep(5)
