# Aiogram imports
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

# Other imports
import asyncio
import logging

# Project imports
from middlewares.dbmiddleware import DbSession
from db.requests import Request


async def sender(bot: Bot, db: DbSession, text_report, mig_rates_buy, mig_rates_sell):
    async with db.connector.acquire() as connect:
        request = Request(connect)

        # Записываем значение валют "МиГ" в таблицу
        for currency, value_rate in mig_rates_buy.items():
            await request.set_last_sent_rates(currency, "buy", value_rate)

        # Записываем значение валют "МиГ" в таблицу
        for currency, value_rate in mig_rates_sell.items():
            await request.set_last_sent_rates(currency, "sell", value_rate)

        if not await request.check_table():
            await request.create_table()
            logging.debug(f"Создана таблица для рассылки")

        users = [result.get("user_id") for result in await request.get_users()]
        logging.debug(f"Список пользователей для рассылки: {users}")

        for row in users:
            try:
                await bot.send_message(chat_id=row, text=text_report)
                await asyncio.sleep(0.05)
                logging.debug(f"Отправляем курсы пользователю {row} по расписанию")

            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                await bot.send_message(chat_id=row, text=text_report)
                logging.debug(f"Превышение лимита, запускаем повторную рассылку")

            except Exception as e:
                await request.set_status(row, "unsuccessful", f"{e}")
                logging.debug(
                    f"Пользователю {row} не смогли отправить сообщение из-за ошибки {e}"
                )

            else:
                await request.set_status(row, "successful", "No error")
                logging.debug(f"Пользователю {row} отправили")

        await request.delete_table()
        logging.debug(f"Удалили таблицу для рассылки")
