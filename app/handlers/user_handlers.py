# Aiogram imports
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

# Other imports
import logging

# Project imports
from lexicon.lexicon import LEXICON_RU
from get_rates.get_report import get_message
from db.requests import Request


# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
async def process_start_command(message: Message, request: Request):
    await request.add_users(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    logging.debug(f"Пользователь {message.from_user.id} добавлен в таблицу users")
    await message.answer(text=LEXICON_RU["/start"])
    text, _, _ = await get_message()
    await message.answer(text=text)
    logging.debug(
        f"Пользователю {message.from_user.id} отправлены курсы при старте бота"
    )


# Этот хэндлер срабатывает на команду /help
@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


# Этот хэндлер срабатывает на команду /send_rates
@user_router.message(Command(commands="send_rates"))
async def process_send_rates_command(message: Message):
    text, _, _ = await get_message()
    await message.answer(text=f'<i>{LEXICON_RU["/send_rates"]}</i>{text}')
    logging.debug(
        f"Пользователю {message.from_user.id} отправлены курсы по команде /send_rates"
    )


# Этот хэндлер будет срабатывать на блокировку бота пользователем
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated, request: Request):
    await request.set_noactive(event.from_user.id)
    logging.debug(f"Пользователь {event.from_user.id} заблокировал бота")


# Этот хэндлер будет срабатывать на разблокировку бота пользователем
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated, request: Request):
    await request.set_active(event.from_user.id)
    logging.debug(f"Пользователь {event.from_user.id} разблокировал бота")
