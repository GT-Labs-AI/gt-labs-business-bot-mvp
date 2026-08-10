import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import config
from app.database.connection import init_db, async_session_maker
from app.middlewares.db import DbSessionMiddleware
from app.utils.logger import setup_logger
from app.handlers import common, appointment, admin


async def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("Initializing database...")
    await init_db()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middlewares
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session_maker))

    # Routers
    dp.include_router(admin.router)       # Admin router checked first
    dp.include_router(common.router)
    dp.include_router(appointment.router)

    logger.info("GT Labs Business Bot started successfully!")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")