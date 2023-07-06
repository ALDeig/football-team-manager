from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.src.services.db.tables import Player


CHECKBOX = {False: "⭕", True: "🔴"}
ACTIONS = {False: "add", True: "remove"}


def kb_select_players(
        players: Sequence[Player],
        selected_players: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for player in players:
        text = f"{CHECKBOX[player.id in selected_players]} {player.name}"
        callback_data = f"{ACTIONS[player.id in selected_players]}:{player.id}"
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.add(InlineKeyboardButton(text="Готово", callback_data="finish"))
    builder.adjust(2)
    return builder.as_markup()

