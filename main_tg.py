"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""

import logging
import os
from dotenv import load_dotenv

from dialogflow import detect_intent_texts
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def reply(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    session_id = f'tg-{os.getenv("ARTSIOM_CHAT_ID")}'
    texts = update.message.text
    language_code = "RU"
    response = detect_intent_texts(project_id, session_id, texts, language_code)

    update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    load_dotenv("./.env")
    tg_api_token = os.getenv("TG_API_KEY")
    updater = Updater(tg_api_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
