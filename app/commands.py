import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.configreader import Config


async def set_commands(bot: Bot, config: Config):
    user_commands = [
        BotCommand(command="start", description="В начало"),
        BotCommand(command="create_teams", description="Создать команды")
    ]
    await bot.set_my_commands(
        commands=user_commands,
        scope=BotCommandScopeDefault()  # type: ignore
    )
    admin_commands = [
        BotCommand(command="start", description="В начало"),
        BotCommand(command="create_teams", description="Создать команды"),
        BotCommand(command="add_player", description="Добавить игрока"),
        BotCommand(command="change_player", description="Изменить уровень игрока"),
        BotCommand(command="delete_player", description="Удалить игрока")
    ]
    for admin_id in config.admins:
        try:
            await bot.set_my_commands(
                commands=admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)  # type: ignore
            )
        except TelegramBadRequest:
            logging.error(f"Can't set commands to admin with ID {admin_id}")

