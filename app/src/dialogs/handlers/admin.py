from typing import cast
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.admin import (
    add_new_player,
    delete_player_by_id,
    reply_kb_for_select_player,
    update_player_level
)


router = Router()


@router.message(Command(commands="start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Работаю...")


@router.message(Command(commands="add_player"))
async def cmd_add_player(msg: Message, state: FSMContext):
    await msg.answer("Введи имя игрока")
    await state.set_state("get_player_name")


@router.message(StateFilter("get_player_name"))
async def get_player_name(msg: Message, state: FSMContext):
    await state.update_data(player_name=msg.text)
    await msg.answer("Введи уровень игрока")
    await state.set_state("get_player_level")


@router.message(StateFilter("get_player_level"), flags={"db": True})
async def get_player_level(msg: Message, db: AsyncSession, state: FSMContext):
    try:
        level = float(cast(str, msg.text))
    except ValueError:
        await msg.answer("Уровень должне быть числом или числом с плавающей точкой")
        return
    data = await state.get_data()
    reply = await add_new_player(db, data["player_name"], level)
    await msg.answer(reply)
    await state.clear()


@router.message(Command(commands="change_player"), flags={"db": True})
async def cmd_change_player(msg: Message, db: AsyncSession, state: FSMContext):
    kb = await reply_kb_for_select_player(db)
    text = "Выберите игрока для изменения уровня"
    await msg.answer(text, reply_markup=kb)
    await state.set_state("select_player_for_change")


@router.callback_query(StateFilter("select_player_for_change"))
async def btn_select_player_for_update(call: CallbackQuery, state: FSMContext):
    if call.message is None or call.data is None: return
    await call.answer()
    await state.update_data(player_id_for_change=call.data)
    await call.message.answer("Введите новый уровень")
    await state.set_state("get_level_for_change_player")


@router.message(StateFilter("get_level_for_change_player"), flags={"db": True})
async def get_level_for_change_player(msg: Message, db: AsyncSession, state: FSMContext):
    try:
        level = float(cast(str, msg.text))
    except ValueError:
        await msg.answer("Уровень должне быть числом или числом с плавающей точкой")
        return
    data = await state.get_data()
    reply = await update_player_level(db, data["player_id_for_change"], level)
    await msg.answer(reply)
    await state.clear()


@router.message(Command(commands="delete_player"), flags={"db": True})
async def cmd_delete_player(msg: Message, db: AsyncSession, state: FSMContext):
    reply_kb = await reply_kb_for_select_player(db)
    text = "Выберите игрока для удаления"
    await msg.answer(text, reply_markup=reply_kb)
    await state.set_state("select_player_for_delete")


@router.callback_query(StateFilter("select_player_for_delete"), flags={"db": True})
async def btn_select_player(call: CallbackQuery, db: AsyncSession, state: FSMContext):
    if call.message is None or call.data is None: return
    reply = await delete_player_by_id(db, call.data)
    await call.message.answer(reply)
    await state.clear()

