from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.confirmation_keyboard import confirmation_keyboard
from states import RegisterState

command_router = Router()


@command_router.message(Command("/shedule"))
async def get_shedule(message: Message):
    pass


@command_router.message(Command("check_registration"))
async def check_registration(message: Message):
    user_id = message.from_user.id


@command_router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    kb = await confirmation_keyboard()
    await state.update_data(user_id=user_id)
    if username:
        await message.answer(f"Вы хотите оставить свое имя пользователя: {message.from_user.username}?", reply_markup=kb)
    else:
        await message.answer("Нет доступа к вашему имени пользователя\nВведите имя пользователя для регистрации")
        await state.set_state(RegisterState.username)
