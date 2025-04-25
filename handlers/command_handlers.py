from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from database.dao_adapter import get_user_info, get_full_schedule
from keyboards.confirmation_keyboard import confirmation_keyboard
from states import RegisterState

command_router = Router()


@command_router.message(Command("schedule"))
async def get_schedule(message: Message):
    pass


@command_router.message(Command("export"))
async def export_schedule(message: Message):
    await get_full_schedule()
    file_path = Path("schedule.json")
    file = FSInputFile(file_path)
    await message.answer_document(file)


@command_router.message(Command("me"))
async def check_registration(message: Message):
    user_id = message.from_user.id
    user_info = await get_user_info(telegram_id=user_id)
    user = user_info.get('user')
    class_ = user_info.get('class')
    await message.answer(f"ID={user.telegram_id}\n"
                         f"Имя пользователя: {user.username}\n"
                         f"Класс: {class_.grade}{class_.identifier}")


@command_router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    kb = await confirmation_keyboard()
    await state.update_data(user_id=user_id)
    if username:
        await message.answer(f"Вы хотите оставить свое имя пользователя: {message.from_user.username}?",
                             reply_markup=kb)
    else:
        await message.answer("Нет доступа к вашему имени пользователя\nВведите имя пользователя для регистрации")
        await state.set_state(RegisterState.username)
