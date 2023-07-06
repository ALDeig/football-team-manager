from collections.abc import Sequence
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.src.services.db.tables import Player


def kb_select_player(players: Sequence[Player]):
    builder = InlineKeyboardBuilder()
    for player in players:
        text = f"{player.name} - {player.level}"
        builder.add(InlineKeyboardButton(text=text, callback_data=player.id))
    builder.adjust(2)
    return builder.as_markup()

