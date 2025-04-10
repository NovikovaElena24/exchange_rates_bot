# Aiogram imports
from aiogram import Bot

# Other imports
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Project imports
from utils.config import config
from middlewares.dbmiddleware import DbSession
from handlers.unscheduled_message import unscheduled_report
from handlers.daily_message import daily_report
from handlers.clear_last_rates import clear_table


async def setup_scheduler(bot: Bot, db: DbSession):

    scheduler = AsyncIOScheduler(timezone=config.tg_timezone.timezone)
    # scheduler.add_job(
    #     unscheduled_report, "interval", seconds=10, kwargs = {"bot": bot, "db": db}
    # )  # Запрос курсов каждый час
    # scheduler.add_job(
    #     # send_daily_report, "interval", seconds=30, kwargs = {"bot": bot, "db": db}
    # )

    scheduler.add_job(
        unscheduled_report,
        "cron",
        kwargs={"bot": bot, "db": db},
        hour="11-20",
        minute="*/30",
    )
    scheduler.add_job(
        daily_report, "cron", kwargs={"bot": bot, "db": db}, hour="11", minute="10"
    )
    scheduler.add_job(clear_table, "cron", kwargs={"db": db}, hour="20", minute="59")

    scheduler.start()
