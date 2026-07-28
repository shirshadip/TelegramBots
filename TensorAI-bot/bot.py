from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import asyncio
import logging

import httpx

from config import *
from ai import ask_ai


logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"
)


conversation_memory = {}


SYSTEM_PROMPT = """
You are a friendly AI assistant.

Always:

- Be helpful.
- Explain clearly.
- Use markdown.
- Answer professionally.
- Keep responses readable.
"""


# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conversation_memory[update.effective_user.id] = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    await update.message.reply_text(

        "👋 Hello!\n\n"
        "I'm your AI assistant.\n\n"
        "Just send me any question."
    )


# -----------------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

"""
Available Commands

/start

/help

/clear

Simply send a message to chat with AI.
"""
    )


# -----------------------------

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conversation_memory[update.effective_user.id] = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    await update.message.reply_text(

        "✅ Conversation cleared."
    )


# -----------------------------

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    text = update.message.text.strip()

    if user not in conversation_memory:

        conversation_memory[user] = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]

    conversation_memory[user].append(

        {
            "role": "user",
            "content": text
        }

    )

    conversation_memory[user] = (
        conversation_memory[user][:1] +
        conversation_memory[user][-MAX_HISTORY:]
    )

    waiting = await update.message.reply_text(
        "🤖 Thinking..."
    )

    try:

        await context.bot.send_chat_action(

            chat_id=update.effective_chat.id,

            action=ChatAction.TYPING
        )

        answer = await ask_ai(
            conversation_memory[user]
        )

        conversation_memory[user].append(

            {
                "role": "assistant",
                "content": answer
            }

        )

        await waiting.edit_text(answer)

    except httpx.TimeoutException:

        await waiting.edit_text(

            "⌛ AI took too long to respond.\nPlease try again."
        )

    except httpx.HTTPStatusError as e:

        if e.response.status_code == 401:

            await waiting.edit_text(
                "❌ Invalid OpenRouter API key."
            )

        elif e.response.status_code == 429:

            await waiting.edit_text(
                "⚠️ Rate limit exceeded.\nPlease wait a minute."
            )

        elif e.response.status_code >= 500:

            await waiting.edit_text(
                "🚧 AI service is temporarily unavailable."
            )

        else:

            await waiting.edit_text(
                "Something went wrong."
            )

    except Exception as e:

        logging.exception(e)

        await waiting.edit_text(

            "❌ Unexpected error occurred."
        )


# -----------------------------

async def error_handler(update, context):

    logging.exception(context.error)


# -----------------------------

def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear))

    app.add_handler(

        MessageHandler(

            filters.TEXT &
            ~filters.COMMAND,

            ai_chat
        )

    )

    app.add_error_handler(error_handler)

    print("AI Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()