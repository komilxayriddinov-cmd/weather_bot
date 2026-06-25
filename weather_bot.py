from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests


TOKEN = "8707168025:AAHEJBxJJ26nPnB0dy16Zdqex4Pwg0qm85o"


cities = [
    ["Toshkent", "Samarqand"],
    ["Buxoro", "Andijon"],
    ["Namangan", "Fargona"]
]

markup = ReplyKeyboardMarkup(cities, resize_keyboard=True)


def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"

    data = requests.get(url).json()

    temp = data["current_condition"][0]["temp_C"]
    desc = data["current_condition"][0]["weatherDesc"][0]["value"]

    return temp, desc


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Shahar tanlang:",
        reply_markup=markup
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text

    try:
        temp, desc = get_weather(city)

        await update.message.reply_text(
            f"🌍 {city}\n\n🌡 Harorat: {temp}°C\n☁️ Holat: {desc}"
        )

    except:
        await update.message.reply_text(
            "Xatolik. Boshqa shahar tanlang."
        )


app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, weather))


print("Погодный бот запущен")

app.run_polling()