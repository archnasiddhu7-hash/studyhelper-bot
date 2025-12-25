import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

# ================= OPENAI CLIENT =================
# OPENAI_API_KEY environment variable se aayegi
client = OpenAI()

# ================= SAFE REPLY (LONG MESSAGE SPLIT) =================
async def safe_reply(update: Update, text: str):
    LIMIT = 4000  # Telegram max ~4096
    for i in range(0, len(text), LIMIT):
        await update.message.reply_text(text[i:i + LIMIT])

# ================= START COMMAND =================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "👋 Hello! Main AI Study Helper Bot hoon 🤖\n\n"
        "📚 Aap mujhse questions pooch sakte ho\n"
        "✍️ Notes, explanation, MCQ, doubt – sab milega\n\n"
        "बस message bhejo 🙂"
    )
    await update.message.reply_text(start_text)

# ================= AI REPLY FUNCTION =================
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        await update.message.chat.send_action("typing")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        reply_text = response.output_text
        await safe_reply(update, reply_text)

    except Exception as e:
        await update.message.reply_text(
            "❌ Kuch error aaya hai. Thodi der baad try karo.\n\n"
            f"Debug: {e}"
        )

# ================= MAIN APP =================
def main():
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN environment variable missing")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .build()
    )

    # /start command
    app.add_handler(CommandHandler("start", start_command))

    # normal text messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply)
    )

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()