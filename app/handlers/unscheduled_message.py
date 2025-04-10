# Aiogram imports
from aiogram import Bot

# Other imports
import logging

# Project imports
from middlewares.dbmiddleware import DbSession
from db.requests import Request
from get_rates.get_rates import get_mig_current_rate
from get_rates.get_report import alarm_mig_rate
from handlers.sender import sender


async def unscheduled_report(bot: Bot, db: DbSession):
    async with db.connector.acquire() as connect:
        request = Request(connect)

        # Получаем курс обменника "МиГ" с сайта https://mig.kz
        new_buy_rates, new_sell_rates = get_mig_current_rate()

        last_buy_rates = await request.get_last_sent_rates("buy")
        last_sell_rates = await request.get_last_sent_rates("sell")

        # Получаем курсы из базы данных (равные последней массовой рассылке)
        last_buy_rates = {
            rates.get("currency"): float(rates.get("value_rate"))
            for rates in last_buy_rates
        }
        logging.debug(f"Курс покупки из базы: {last_buy_rates}")

        last_sell_rates = {
            rates.get("currency"): float(rates.get("value_rate"))
            for rates in last_sell_rates
        }
        logging.debug(f"Курс продажи из базы: {last_sell_rates}")

        limit_percent = 0.01

        # Если значение какого-либо курса изменилось на >= 1% относительно последнего из массовой рассылки, то делаем новую рассылку
        if new_buy_rates and last_buy_rates:
            flag_buy = any(
                map(
                    lambda currency: abs(
                        new_buy_rates[currency] - last_buy_rates[currency]
                    )
                    / last_buy_rates[currency]
                    >= limit_percent,
                    new_buy_rates,
                )
            )
            flag_sell = any(
                map(
                    lambda currency: abs(
                        new_sell_rates[currency] - last_sell_rates[currency]
                    )
                    / last_sell_rates[currency]
                    >= limit_percent,
                    new_sell_rates,
                )
            )
            if flag_buy or flag_sell:
                message = await alarm_mig_rate(
                    new_buy_rates, new_sell_rates, last_buy_rates, last_sell_rates
                )
                logging.debug(
                    f"Сформировано внеплановое сообщение для рассылки из-за изменения курса"
                )
                await sender(bot, db, message, new_buy_rates, new_sell_rates)
