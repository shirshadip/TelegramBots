# ==============================
# Telegram Bot Boilerplate
# ==============================

from telegram import Update
import json
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

# Bot Token
with open ("config.json", "r") as f:
    config = json.load(f)
TOKEN = config["BOT_TOKEN"]


# ------------------------------
# Commands
# ------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Runs when user sends /start"""
    await update.message.reply_text("Hello! 👋")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Runs when user sends /help"""
    await update.message.reply_text("Available commands:\n/start\n/help\n/hi")

async def hi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("hi")


# ------------------------------
# Message Handler
# ------------------------------

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Replies with the same message"""
    await update.message.reply_text(update.message.text)


# ------------------------------
# Main Function
# ------------------------------

def main():

    # Create bot application
    app = Application.builder().token(TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hi", hi_command))

    # Register message handler
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    # Start bot
    print("Bot is running...")
    app.run_polling()


# ------------------------------
# Run Program
# ------------------------------

if __name__ == "__main__":
    main()