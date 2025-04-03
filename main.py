import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from handlers.callback_handlers import callback_router
from handlers.command_handlers import command_router
from handlers.state_handlers import state_router

token = "8088850105:AAH79luOLJ3KVZJ89SlHq71m3YFtcnmzD8Y"

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет. Я бот с расписанием твоей школы."
        "Введи команду /shedule чтобы начать.")


async def main():
    dp.include_routers(command_router, state_router, callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
