from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_create_poll = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Добавить опрос", callback_data="add_poll")]]
)

def kb_again_shuffle_teams():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перемешать", callback_data="again_shuffle")]
        ]
    )
    return kb

