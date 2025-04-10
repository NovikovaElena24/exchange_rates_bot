# Aiogram imports
from aiogram import Bot

# Other imports
import logging

# Project imports
from get_rates.get_report import get_message
from middlewares.dbmiddleware import DbSession
from handlers.sender import sender


async def daily_report(bot: Bot, db: DbSession):
    message, mig_rates_buy, mig_rates_sell = await get_message()
    text = f"🔔<i>Ежедневное оповещение</i>\n\n" + message
    logging.debug(f"Старт ежедневной рассылки")
    await sender(bot, db, text, mig_rates_buy, mig_rates_sell)
