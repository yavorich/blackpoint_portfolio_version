from telegram import InlineKeyboardMarkup

from apps.account.buttons.start import get_start_buttons


def get_start_markup(user):
    start_buttons = get_start_buttons(uuid=user.uuid)
    return InlineKeyboardMarkup(
        [
            [
                start_buttons["start_mini_app"],
            ],
        ]
    )
