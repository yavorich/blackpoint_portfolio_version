import logging

from telegram.ext import (
    ApplicationBuilder,
    PicklePersistence,
)
from telegram import Update
from config.settings import MAIN_TELEGRAM_BOT_TOKEN
from telegram_bot.main.endpoints import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)


def main():
    main_persistence = PicklePersistence(
        filepath="persistence.pyc",
    )
    application = (
        ApplicationBuilder()
        .token(MAIN_TELEGRAM_BOT_TOKEN)
        .persistence(main_persistence)
        .build()
    )
    application.add_handlers(handlers)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
