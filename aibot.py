import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# OpenAI client (API key env se aayegi)
client = OpenAI()

# ---------- START COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Main AI Study Helper Bot hoon 🤖\n\n"
        "📚 Question bhejo, main help karunga 🙂"
    )

# ---------- CHAT HANDLER ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.chat.send_action("typing")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=update.message.text
        )

        await update.message.reply_text(response.output_text)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ---------- MAIN ----------
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
