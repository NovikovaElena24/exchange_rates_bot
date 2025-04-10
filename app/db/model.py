# Project imports
from middlewares.dbmiddleware import DbSession


async def create_tables(db: DbSession):
    async with db.connector.acquire() as connect:

        await connect.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT NOT NULL,
            user_name TEXT,
            first_name TEXT,
            last_name TEXT,
            active INTEGER,
            PRIMARY KEY (user_id)
        )
        """
        )

        await connect.execute(
            """
        CREATE TABLE IF NOT EXISTS last_sent_rates (
            currency TEXT NOT NULL,
            type_rate TEXT NOT NULL,
            value_rate NUMERIC,
            PRIMARY KEY (currency, type_rate)
        )
        """
        )
