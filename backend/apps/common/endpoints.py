from telegram.ext import MessageHandler, filters

from apps.common.handlers.unknown import unknown


handlers = [
    MessageHandler(filters.COMMAND, unknown),
]
