# Aiogram imports
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Other imports
import asyncio
import asyncpg
import logging

# Project imports
from utils.config import config
from handlers import other_handlers, user_handlers
from scheduler.scheduler import setup_scheduler
from keyboards.set_menu import set_main_menu
from middlewares.dbmiddleware import DbSession
from db.model import create_tables


async def create_pool():
    logging.debug(f"Connecting to database at {config.db.db_user}:{config.db.db_password}:{config.db.db_database}:{config.db.db_host}:{config.db.db_port}")
    return await asyncpg.create_pool(
        user=config.db.db_user,
        password=config.db.db_password,
        database=config.db.db_database,
        host=config.db.db_host,
        port=config.db.db_port,
        command_timeout="60",
    )


# Функция конфигурирования и запуска бота
async def main():

    logging.basicConfig(
        # filename='app.log',  # Имя файла для записи логов
        # filemode='a',        # Режим открытия файла ('a' для добавления, 'w' для перезаписи)
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        timeout=20,
    )
    # Создаем pool соединений с базой данных
    pool_connect = await create_pool()
    db = DbSession(pool_connect)

    # Создаем таблицы
    await create_tables(db)

    # Инициализируем диспетчер
    dp = Dispatcher()

    # Регистрируем middleware на все типы событий
    dp.update.middleware.register(db)

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.user_router)
    dp.include_router(other_handlers.othet_router)

    await setup_scheduler(bot, db)

    # Пропускаем накопившиеся апдейты и запускаем polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
