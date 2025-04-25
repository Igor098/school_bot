import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from config import bot_token
from database.dao_adapter import check_register
from handlers.callback_handlers import callback_router
from handlers.command_handlers import command_router
from handlers.file_handlers import file_router
from handlers.state_handlers import state_router

from loguru import logger

token = bot_token

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    is_registered = await check_register(telegram_id=message.from_user.id)
    if is_registered:
        await message.answer(
            "Привет. Я бот с расписанием твоей школы. "
            "Введи команду /shedule чтобы начать.")
    else:
        await message.answer(
            "Привет. Я бот с расписанием твоей школы. "
            "Для начала работы нужно зарегистрироваться. "
            "Введи команду: /register")


async def main():
    logger.info("Бот запущен")
    dp.include_routers(command_router, state_router, callback_router, file_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
