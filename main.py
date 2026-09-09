import os
import logging
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured.")


WELCOME_TEXT = """
👋 Welcome to Sabong24hBot!

I'm your simple assistant for quick answers and helpful information.

You can ask a question or choose an option below.
"""


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📋 FAQ", callback_data="faq"),
            InlineKeyboardButton("📞 Contact", callback_data="contact"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        text = """
ℹ️ About Sabong24hBot

Sabong24hBot is a simple assistant designed to provide quick answers, helpful information, and easy navigation.

Ask a question or use the menu to explore the available options.
"""

    elif query.data == "help":
        text = """
❓ How to use the bot

Simply type your question and send it.

You can also use the buttons in the menu to view information, FAQs, and help.
"""

    elif query.data == "faq":
        text = """
📋 Frequently Asked Questions

Q: What does this bot do?
A: It provides simple information and answers to common questions.

Q: How do I use the bot?
A: Send a question or choose an option from the menu.

Q: Can I contact someone?
A: Use the Contact option for available contact information.
"""

    elif query.data == "contact":
        text = """
📞 Contact

If you need assistance, please use the available contact information provided by the administrator.

Thank you for using Sabong24hBot.
"""

    else:
        text = "Please choose an option from the menu."

    await query.edit_message_text(
        text,
        reply_markup=main_menu(),
    )


def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = clean_text(update.message.text)

    if any(word in user_text for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        await update.message.reply_text(
            "👋 Hello! Welcome to Sabong24hBot. How can I help you?",
            reply_markup=main_menu(),
        )
        return

    if "what can you do" in user_text or "what do you do" in user_text:
        await update.message.reply_text(
            "🤖 I can provide simple information, answer common questions, and help you navigate the available options."
        )
        return

    if "about" in user_text:
        await update.message.reply_text(
            "ℹ️ Sabong24hBot is a simple assistant for quick answers, helpful information, and easy navigation."
        )
        return

    if "help" in user_text:
        await update.message.reply_text(
            "❓ Send me a question or use the menu buttons to find information."
        )
        return

    if "thank" in user_text:
        await update.message.reply_text(
            "You're welcome! 😊"
        )
        return

    if "bye" in user_text or "goodbye" in user_text:
        await update.message.reply_text(
            "Goodbye! 👋 Thanks for using Sabong24hBot."
        )
        return

    await update.message.reply_text(
        "Sorry, I don't have an answer for that question yet. "
        "Please try another question or choose an option from the menu.",
        reply_markup=main_menu(),
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question)
    )

    print("Sabong24hBot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
