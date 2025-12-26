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

# ================= OPENAI CLIENT =================
client = OpenAI()

# ================= SAFE REPLY =================
async def safe_reply(update: Update, text: str):
    LIMIT = 4000
    for i in range(0, len(text), LIMIT):
        await update.message.reply_text(text[i:i + LIMIT])

# ================= START =================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Main AI Study Helper Bot hoon 🤖\n\n"
        "📚 Questions, notes, MCQ, explanation – sab milega\n\n"
        "बस message bhejo 🙂"
    )

# ================= AI REPLY =================
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

# ================= MAIN =================
async def main():
