import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
application = Application.builder().token(TOKEN).build()

CAR_BRANDS = ["Daewoo", "ZAZ", "Lada"]

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я — АвтоПомічник. Напиши /choosecar щоб вибрати авто.")

async def choosecar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"Обрати {brand}", callback_data=f"brand_{brand}")] for brand in CAR_BRANDS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть марку авто:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand = query.data.replace("brand_", "")
    await query.message.reply_text(f"Ти вибрав: {brand}")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("choosecar", choosecar))
application.add_handler(CallbackQueryHandler(handle_callback))
