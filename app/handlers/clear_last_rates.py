# Other imports
import logging

# Project imports
from middlewares.dbmiddleware import DbSession
from db.requests import Request


async def clear_table(db: DbSession):
    async with db.connector.acquire() as connect:
        request = Request(connect)

        await request.clear_last_sent_rates()
        logging.debug(f"Таблица с последними значениями курсов очищена")
