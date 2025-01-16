from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import ContextTypes

from apps.account.markups.start import get_start_markup
from apps.account.messages.start import START_MESSAGES
from apps.account.models import User
from apps.account.services.get_avatar import get_avatar
from core.utils.random_string import generate_random_string


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.from_user

    user = await User.objects.filter(telegram_id=user_data.id).afirst()

    if not user:
        username = user_data.username or f"user_{generate_random_string()}"

        user = await User.objects.acreate(
            telegram_id=user_data.id,
            username=username,
            first_name=user_data.first_name or "",
            last_name=user_data.last_name or "",
            avatar=await get_avatar(update, context),
        )

        await user.asave()

    context.user_data["django_user"] = user

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGES["hello"],
        reply_markup=get_start_markup(context.user_data["django_user"]),
        parse_mode=ParseMode.HTML,
    )
