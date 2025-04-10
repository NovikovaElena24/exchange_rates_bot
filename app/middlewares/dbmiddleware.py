# Aiogram imports
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# Other imports
from typing import Callable, Awaitable, Dict, Any
import asyncpg

# Project imports
from db.requests import Request


class DbSession(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool):
        super().__init__()
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.connector.acquire() as connect:
            data["request"] = Request(connect)
            result = await handler(event, data)
            return result
