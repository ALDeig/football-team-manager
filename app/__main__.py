import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from app.settings import settings, logging_setup
from app.commands import set_commands
from app.src.dialogs.handlers import admin, user
from app.src.middleware.db import DbSessionMiddleware
from app.src.services.db.db_connect import create_session_factory


logging_setup()
logger = logging.getLogger(__name__)


def include_routers(dp: Dispatcher):
    dp.include_router(admin.router)
    dp.include_router(user.router)


def include_filters(admins: list[int], dp: Dispatcher):
    dp.message.filter(F.chat.type == "private")
    admin.router.message.filter(F.chat.id.in_(admins))


async def main():
    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    if settings.bot_fsm_storage == "redis":
        raise ValueError("redis is not install")
    else:
        storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    if settings.sqlite_dsn is None:
        raise ValueError("sqlite_dsn not avalible")
    session_factory = create_session_factory(settings.sqlite_dsn)

    # Регистрация фильтров
    include_filters(settings.admins, dp)

    # Регистрация middlewares
    dp.message.middleware(DbSessionMiddleware(session_factory))
    dp.callback_query.middleware(DbSessionMiddleware(session_factory))

    # Регистрация хендлеров
    include_routers(dp)

    # Установка команд для бота
    await set_commands(bot, settings)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        logger.info("Bot starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Bot stopping...")
