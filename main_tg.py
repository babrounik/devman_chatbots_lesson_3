"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""
import argparse
import os
from functools import partial
from dotenv import load_dotenv

from dialogflow import detect_intent_texts
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext, _project_id, _language_code) -> None:
    response = detect_intent_texts(_project_id, update.effective_user, update.message.text, _language_code)
    update.message.reply_text(response)


def main() -> None:
    """Start the bot."""

    load_dotenv("./.env")
    tg_api_token = os.getenv("TG_API_KEY")
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    language_code = "RU"
    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, partial(reply,
                                                                _project_id=project_id,
                                                                _language_code=language_code))
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
