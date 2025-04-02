from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

from states import RegisterState

callback_router = Router()


@callback_router.callback_query(F.data == "confirm")
async def confirm(callback: CallbackQuery, state: FSMContext):

    await state.update_data(username=callback.from_user.username)
    await callback.answer("Принято")
    await state.set_state(RegisterState.class_number)
    await callback.message.answer("Введите номер класса без буквы")


@callback_router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer("Введите имя пользователя:")
    await state.set_state(RegisterState.username)
