import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

client = OpenAI()

async def safe_reply(update: Update, text: str):
    LIMIT = 4000
    for i in range(0, len(text), LIMIT):
        await update.message.reply_text(text[i:i + LIMIT])

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Main AI Study Helper Bot hoon 🤖\n\n"
        "📚 Questions, notes, MCQ, explanation – sab milega\n\n"
        "बस message bhejo 🙂"
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.chat.send_action("typing")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=update.message.text
        )

        await safe_reply(update, response.output_text)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("🤖 Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
