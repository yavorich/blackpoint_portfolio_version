from telegram.ext import CommandHandler

from apps.account.handlers.start import start


handlers = [
    CommandHandler("start", start),
]
