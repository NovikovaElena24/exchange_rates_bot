# Aiogram imports
from aiogram import Router
from aiogram.types import Message

# Other imports
import logging

# Project imports
from lexicon.lexicon import LEXICON_RU


# Инициализируем роутер уровня модуля
othet_router = Router()


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@othet_router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON_RU["no_answer"])
    logging.debug(f"Пользователь {message.from_user.id} ввел некорректную команду")
