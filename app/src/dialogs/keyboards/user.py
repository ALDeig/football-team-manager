from app.settings import settings 

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_after_created_teams(user_id: int, state_level: str) -> InlineKeyboardMarkup:
    inline_keyboard=[
        [InlineKeyboardButton(text="Перемешать", callback_data="again_shuffle")]
    ]
    if user_id in settings.admins:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text="Скрыть" if state_level == "show" else "Показать",
                callback_data="hide" if state_level == "show" else "show"
            )]
        )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return kb
