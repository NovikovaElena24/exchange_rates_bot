# Other imports
import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_users(self, user_id, user_name, first_name, last_name):
        query = (
            f"INSERT INTO users (user_id, user_name, first_name, last_name, active) "
            f"VALUES({user_id}, '{user_name}', '{first_name}', '{last_name}', 1) "
            f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}', first_name='{first_name}', last_name='{last_name}';"
        )
        await self.connector.execute(query)

    async def set_active(self, user_id):
        query = f"UPDATE users SET active = 1 WHERE user_id = {user_id};"
        await self.connector.execute(query)

    async def set_noactive(self, user_id):
        query = f"UPDATE users SET active = 0 WHERE user_id = {user_id};"
        await self.connector.execute(query)

    async def check_table(self):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users_for_sender');"
        return await self.connector.fetchval(query)

    async def create_table(self):
        query = f"CREATE TABLE users_for_sender (user_id bigint NOT NULL, status text, description text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)
        query = f"INSERT INTO users_for_sender (user_id, status, description) SELECT user_id, 'waiting', null FROM users WHERE active=1"
        await self.connector.execute(query)

    async def delete_table(self):
        query = f"DROP TABLE users_for_sender;"
        await self.connector.execute(query)

    async def get_users(self):
        query = f"SELECT user_id FROM users_for_sender WHERE status='waiting';"
        return await self.connector.fetch(query)

    async def set_status(self, user_id, status, descriotion):
        query = f"UPDATE users_for_sender SET status='{status}', description='{descriotion}' WHERE user_id={user_id};"
        await self.connector.execute(query)

    async def set_last_sent_rates(self, currency, type_rate, value_rate):
        query = (
            f"INSERT INTO last_sent_rates(currency, type_rate, value_rate) "
            f"VALUES ('{currency}', '{type_rate}', {value_rate}) "
            f"ON CONFLICT (currency, type_rate) DO UPDATE SET value_rate={value_rate};"
        )
        await self.connector.execute(query)

    async def get_last_sent_rates(self, type_rate):
        query = f"SELECT currency, value_rate FROM last_sent_rates WHERE type_rate='{type_rate}';"
        return await self.connector.fetch(query)

    async def clear_last_sent_rates(self):
        await self.connector.execute("DELETE FROM last_sent_rates")
