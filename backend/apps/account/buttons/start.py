from telegram import InlineKeyboardButton, WebAppInfo

from config.settings import MINI_APP_URL


def get_start_buttons(uuid):
    return {
        "start_mini_app": InlineKeyboardButton(
            text="Запустить приложение",
            web_app=WebAppInfo(
                MINI_APP_URL.format(uuid=uuid),
            ),
        )
    }
