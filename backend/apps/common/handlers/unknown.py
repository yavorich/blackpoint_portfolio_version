from telegram import Update
from telegram.ext import ContextTypes

from apps.common.messages.common import COMMON_MESSAGES


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=COMMON_MESSAGES["unknown"],
    )
