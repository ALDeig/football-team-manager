import enum
from aiogram import F, Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.kb_create_team import kb_select_players
from app.src.dialogs.keyboards.user import kb_after_created_teams
from app.src.services.db import db_requests
from app.src.services.teams import create_team_text, create_teams


router = Router()


@router.message(Command(commands="start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Работаю...")


@router.message(Command(commands="create_teams"))
async def cmd_create_teams(msg: Message, state: FSMContext):
    await msg.answer("Введи количество команд")
    await state.set_state("get_number_of_teams")


@router.message(StateFilter("get_number_of_teams"), flags={"db": True})
async def get_number_of_teams(msg: Message, db: AsyncSession, state: FSMContext):
    if msg.text is None or not msg.text.isdigit():
        await msg.answer("Количество должно быть числом")
        return
    players = await db_requests.get_players(db)
    kb = kb_select_players(players, [])
    await msg.answer("Выбери игроков", reply_markup=kb)
    msg_amount_players = await msg.answer("Количество выбранных игроков - 0")
    await state.update_data(
        players=players,
        selected_players=[],
        num_of_teams=int(msg.text),
        msg_amount_players=msg_amount_players.message_id,
    )
    await state.set_state("select_players")


# @router.message(Command(commands="create_teams"), flags={"db": True})
# async def cmd_create_teams(msg: Message, db: AsyncSession, state: FSMContext):
#     players = await db_requests.get_players(db)
#     await state.update_data(players=players, selected_players=[])
#     kb = kb_select_players(players, [])
#     await msg.answer("Выбери игроков", reply_markup=kb)
#     await state.set_state("select_players")


@router.callback_query(
    StateFilter("select_players"), F.data.in_(("finish", "again_shuffle"))
)
async def btn_finish_players_select(call: CallbackQuery, state: FSMContext):
    if call.message is None:
        return
    data = await state.get_data()
    teams = create_teams(
        data["num_of_teams"], data["players"], data["selected_players"]
    )
    texts = [
        create_team_text(number, team, "hide") for number, team in enumerate(teams, 1)
    ]
    msgs_teams = []
    for text in texts[:-1]:
        msg = await call.message.answer(text)
        msgs_teams.append(msg.message_id)
    msg_last_team = await call.message.answer(
        texts[-1], reply_markup=kb_after_created_teams(call.from_user.id, "hide")
    )
    msgs_teams.append(msg_last_team.message_id)
    await state.update_data(teams=teams, msgs_teams=msgs_teams)


@router.callback_query(StateFilter("select_players"), F.data.in_(("hide", "show")))
async def btn_show_or_hide_team_level(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data is None or call.message is None:
        return
    await call.answer()
    data = await state.get_data()
    texts = [
        create_team_text(number, team, call.data)
        for number, team in enumerate(data["teams"], 1)
    ]
    for index, text in enumerate(texts[:-1]):
        await bot.edit_message_text(text, call.from_user.id, data["msgs_teams"][index])
    await bot.edit_message_text(
        text=texts[-1],
        chat_id=call.from_user.id,
        message_id=data["msgs_teams"][-1],
        reply_markup=kb_after_created_teams(call.from_user.id, call.data),
    )


@router.callback_query(StateFilter("select_players"))
async def btn_select_player(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data is None or call.message is None:
        return
    action, player_id = call.data.split(":")
    data = await state.get_data()
    selected_players: list[str] = data["selected_players"]
    if action == "add":
        selected_players.append(player_id)
    else:
        selected_players.pop(selected_players.index(player_id))
    kb = kb_select_players(data["players"], selected_players)
    await call.message.edit_reply_markup(reply_markup=kb)
    await bot.edit_message_text(
        f"Количество выбранных игроков - {len(selected_players)}",
        call.from_user.id,
        data["msg_amount_players"],
    )
