from telegram.ext import Application, CommandHandler
import datetime
import requests
# put your token here
TOKEN = "8210579612:AAFvRhaJTAuEWtHCz0UXZY1MY1RJAI21cU4"
API_KEY = "e74af747e1077d2ba194d181cd9c4bde"
API_KEY_CURRENCY = "a4a39a7eefd3c1b698950f02c3cb742b"
# command handlers
async def start(update, context):
    await update.message.reply_text("👋 Hello! I am your helpful bot.")

async def now(update, context):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"⏰ Current time: {current_time}")

async def help_command(update, context):
    help_text = (
        "📌 Here are the commands you can use:\n\n"
        "/start - Start the bot\n"
        "/now - Show current time\n"
        "/weather <city> - Get weather info for a city\n"
        "/currency <FROM> <TO> - Convert between currencies (e.g. /currency USD UZS)\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)

async def weather(update, context):
    if not context.args:
        await update.message.reply_text("🌤️ Please provide a city name.\nExample: /weather Tashkent")
        return
    
    city = " ".join(context.args)  # get city name from user input
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await update.message.reply_text("⚠️ City not found. Try again.")
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].title()
        feels_like = data["main"]["feels_like"]

        message = (
            f"🌍 Weather in {city.title()}:\n"
            f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"☁️ Condition: {description}"
        )

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text("⚠️ Could not fetch weather. Please try again later.")

async def currency(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("💱 Usage: /currency USD UZS")
        return

    from_currency = context.args[0].upper()
    to_currency = context.args[1].upper()

    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount=1&access_key={API_KEY_CURRENCY}"

    try:
        response = requests.get(url)
        data = response.json()

        # check success
        if not data.get("success", True):
            error_info = data.get("error", {}).get("info", "Unknown error")
            await update.message.reply_text(f"⚠️ API error: {error_info}")
            return

        rate = data.get("result")
        if rate is None:
            await update.message.reply_text("⚠️ Could not fetch currency data. Check your symbols.")
            return

        message = f"💱 1 {from_currency} = {rate:.2f} {to_currency}"
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error while fetching currency data: {e}")



def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("now", now))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("currency", currency))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


    
