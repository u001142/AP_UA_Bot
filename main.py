import os
from fastapi import FastAPI, Request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
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

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{WEBHOOK_SECRET}")

@app.post(f"/{{secret}}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"status": "forbidden"}
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

# Команди
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я — АвтоПомічникUA. Я допоможу тобі з ремонтом будь-якого авто. "
        "Введи команду /setcar, щоб обрати своє авто.")

async def setcar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        car = " ".join(context.args)
        database.set_user_car(user_id, car)
        await update.message.reply_text(f"Твоє авто збережено: {car}")
    else:
        await update.message.reply_text("Використай команду так: /setcar марка модель рік")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    car = database.get_user_car(user_id)
    if not car:
        await update.message.reply_text("Спочатку введи своє авто командою /setcar.")
        return
    question = update.message.text.replace("/ask", "").strip()
    if not question:
        await update.message.reply_text("Введи запит після команди /ask.")
        return
    full_prompt = f"Автомобіль: {car}\\nПитання: {question}\\n\\nДай докладну відповідь українською."

    answer = openai_api.ask_ai(full_prompt)
    await update.message.reply_text(answer)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("setcar", setcar))
application.add_handler(CommandHandler("ask", ask))
