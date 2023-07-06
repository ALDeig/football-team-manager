from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.kb_admin import kb_select_player
from app.src.services.db import db_requests


async def add_new_player(session: AsyncSession, name: str, level: float) -> str:
    await db_requests.add_player(session, name, level)
    text = f"Игрок: <b>{name}</b>\nУровень: <b>{level}</b>"
    return text


async def reply_kb_for_select_player(session: AsyncSession) -> InlineKeyboardMarkup:
    players = await db_requests.get_players(session)
    kb = kb_select_player(players)
    # text = "Выберите игрока для изменения"
    # await state.update_data(players=players)
    return kb


async def update_player_level(session: AsyncSession, player_id: str, level: float) -> str:
    await db_requests.update_player(session, player_id, {"level": level})
    return "Готово"


async def delete_player_by_id(session: AsyncSession, player_id: str) -> str:
    await db_requests.delete_player(session, player_id)
    return "Готово"
