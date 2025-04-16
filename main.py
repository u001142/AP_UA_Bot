import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
from dotenv import load_dotenv
import database
import openai_api

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
application = Application.builder().token(TOKEN).build()

# Стани для діалогу
USER_STATE = {}

# 20 популярних марок авто + посилання на лого
CAR_BRANDS = {
    "Toyota": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Toyota_logo.png",
    "BMW": "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
    "Mercedes": "https://upload.wikimedia.org/wikipedia/commons/9/90/Mercedes-Logo.svg",
    "Audi": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Audi_logo.png",
    "Volkswagen": "https://upload.wikimedia.org/wikipedia/commons/3/34/VW_Logo.png",
    "Ford": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Ford_logo_flat.svg",
    "Honda": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Honda_logo.svg",
    "Hyundai": "https://upload.wikimedia.org/wikipedia/commons/8/88/Hyundai_logo.svg",
    "Kia": "https://upload.wikimedia.org/wikipedia/commons/7/74/Kia_logo3.png",
    "Chevrolet": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Chevrolet_logo.png",
    "Mazda": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Mazda_logo.png",
    "Nissan": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Nissan_2020_logo.svg",
    "Peugeot": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Peugeot_Logo_2021.png",
    "Renault": "https://upload.wikimedia.org/wikipedia/commons/5/58/Renault_2021_logo.svg",
    "Skoda": "https://upload.wikimedia.org/wikipedia/commons/8/84/Skoda_Auto_logo.png",
    "Opel": "https://upload.wikimedia.org/wikipedia/commons/8/88/Opel_Logo_2021.png",
    "Volvo": "https://upload.wikimedia.org/wikipedia/commons/6/66/Volvo_Iron_Mark.png",
    "Lexus": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Lexus_division_emblem.svg",
    "Mitsubishi": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Mitsubishi_logo.png",
    "Subaru": "https://upload.wikimedia.org/wikipedia/commons/8/84/Subaru_logo.png",
}

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{WEBHOOK_SECRET}")

@app.post("/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"status": "forbidden"}
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

# Команди
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я — АвтоПомічникUA. Введи /choosecar щоб обрати авто або /setcar вручну.")

async def setcar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        car = " ".join(context.args)
        database.set_user_car(user_id, car)
        await update.message.reply_text(f"Твоє авто збережено: {car}")
    else:
        await update.message.reply_text("Використай команду так: /setcar марка модель рік")

async def choosecar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for brand, logo_url in CAR_BRANDS.items():
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Вибрати {brand}", callback_data=f"brand_{brand}")]
        ])
        await update.message.reply_photo(photo=logo_url, caption=brand, reply_markup=button)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data.startswith("brand_"):
        brand = data.split("_", 1)[1]
        USER_STATE[user_id] = {"brand": brand, "awaiting_model": True}
        await query.message.reply_text(f"Введи модель і рік для {brand} (наприклад: Camry 2010)")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    car = database.get_user_car(user_id)
    if not car:
        await update.message.reply_text("Спочатку введи своє авто командою /setcar або /choosecar.")
        return

    question = update.message.text.replace("/ask", "").strip()
    if not question:
        await update.message.reply_text("Введи запит після команди /ask.")
        return

    full_prompt = f"Автомобіль: {car}\nПитання: {question}\n\nДай докладну відповідь українською."
    answer = openai_api.ask_ai(full_prompt)
    await update.message.reply_text(answer)

# Обробка відповіді після вибору бренду
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id in USER_STATE and USER_STATE[user_id].get("awaiting_model"):
        brand = USER_STATE[user_id]["brand"]
        full_car = f"{brand} {text}"
        database.set_user_car(user_id, full_car)
        await update.message.reply_text(f"Твоє авто збережено: {full_car}")
        USER_STATE.pop(user_id)
    else:
        await update.message.reply_text("Щоб поставити питання, спочатку задай авто через /setcar або /choosecar.")

# Хендлери
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("setcar", setcar))
application.add_handler(CommandHandler("choosecar", choosecar))
application.add_handler(CommandHandler("ask", ask))
application.add_handler(CallbackQueryHandler(button_callback))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
