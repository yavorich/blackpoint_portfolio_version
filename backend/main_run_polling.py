import logging
from asgiref.sync import sync_to_async

from telegram.ext import (
    ApplicationBuilder,
    PicklePersistence,
)
from telegram import ChatMember, ChatMemberUpdated, Update
from config.settings import MAIN_TELEGRAM_BOT_TOKEN
from telegram_bot.main.endpoints import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


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
