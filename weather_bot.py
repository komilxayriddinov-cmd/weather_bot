from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests


TOKEN = "8707168025:AAHEJBxJJ26nPnB0dy16Zdqex4Pwg0qm85o"


cities = [
    ["Toshkent", "Samarqand", "Buxoro"],
    ["Andijon", "Namangan", "Fargona"],
    ["Nukus", "Xiva", "Urganch"],
    ["Qarshi", "Termiz", "Navoiy"],
    ["Jizzax", "Guliston", "Qo'qon"]
]

markup = ReplyKeyboardMarkup(cities, resize_keyboard=True)


def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"

    data = requests.get(url).json()

    current = data["current_condition"][0]

    temp = current["temp_C"]
    desc = current["weatherDesc"][0]["value"]
    wind = current["windspeedKmph"]
    humidity = current["humidity"]

    forecast = data["weather"]

    return temp, desc, wind, humidity, forecast


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 Shaharni tanlang:",
        reply_markup=markup
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text

    try:
        temp, desc, wind, humidity, forecast = get_weather(city)

        await update.message.reply_text(
            f"🌍 {city}\n\n"
            f"🌡 Hozirgi harorat: {temp}°C\n"
            f"☁️ Holat: {desc}\n"
            f"💨 Shamol: {wind} km/soat\n"
            f"💧 Namlik: {humidity}%\n\n"
            f"📅 Ertaga:\n"
            f"🌡 {forecast[1]['mintempC']}°C - {forecast[1]['maxtempC']}°C\n\n"
            f"📅 2 kundan keyin:\n"
            f"🌡 {forecast[2]['mintempC']}°C - {forecast[2]['maxtempC']}°C"
        )

    except:
        await update.message.reply_text(
            "❌ Xatolik. Boshqa shahar tanlang."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, weather))

print("🌤 Ob-Havo bot ishga tushdi")

app.run_polling()
