from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.kb_create_team import kb_select_players
from app.src.dialogs.keyboards.user import kb_again_shuffle_teams
from app.src.services.db import db_requests
from app.src.services.teams import create_teams


router = Router()


@router.message(Command(commands="start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Работаю...")


@router.message(Command(commands="create_teams"), flags={"db": True})
async def cmd_create_teams(msg: Message, db: AsyncSession, state: FSMContext):
    players = await db_requests.get_players(db)
    await state.update_data(players=players, selected_players=[])
    kb = kb_select_players(players, [])
    await msg.answer("Выбери игроков", reply_markup=kb)
    await state.set_state("select_players")


@router.callback_query(
    StateFilter("select_players"),
    F.data.in_(("finish", "again_shuffle"))
)
async def btn_finish_players_select(call: CallbackQuery, state: FSMContext):
    if call.message is None: return
    data = await state.get_data()
    text_1, text_2 = create_teams(data["players"], data["selected_players"])
    await call.message.answer(text_1)
    await call.message.answer(text_2, reply_markup=kb_again_shuffle_teams())
    # await state.clear()


@router.callback_query(StateFilter("select_players"))
async def btn_select_player(call: CallbackQuery, state: FSMContext):
    if call.data is None or call.message is None: return
    action, player_id = call.data.split(":")
    data = await state.get_data()
    selected_players: list[str] = data["selected_players"]
    if action == "add":
        selected_players.append(player_id)
    else:
        selected_players.pop(selected_players.index(player_id))
    kb = kb_select_players(data["players"], selected_players)
    await call.message.edit_reply_markup(reply_markup=kb)

