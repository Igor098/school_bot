import json
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import Null, select

from database.dao import UserDAO
from database.dao_adapter import find_user_by_telegram_id, find_class
from database.models import User, Class, UserClass
from dependencies.dao_dep import get_session_with_commit
from exceptions.user_exceptions import ClassNotFoundException, UserRegisteredException
from states import RegisterState
from loguru import logger


state_router = Router()


@state_router.message(RegisterState.username)
async def set_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите номер класса без буквы")
    await state.set_state(RegisterState.class_number)


@state_router.message(RegisterState.class_number)
async def set_class_number(message: Message, state: FSMContext):
    await state.update_data(class_number=message.text)
    await message.answer("Введите букву класса")
    await state.set_state(RegisterState.class_identifier)
    
    
@state_router.message(RegisterState.class_identifier)
async def set_class_identifier(message: Message, state: FSMContext):
    await state.update_data(class_identifier=message.text.upper())
    data = await state.get_data()
    logger.info(data)

    user_id = data.get("user_id")
    username = data.get("username")
    class_number = data.get("class_number")
    class_identifier = data.get("class_identifier", None)

    try:
        result = await find_user_by_telegram_id(user_id)
        logger.info("user_answer", result)
        if result:
            raise UserRegisteredException

        result = await find_class(int(class_number), class_identifier)
        class_ = result.scalars().first()

        if not class_:
            raise ClassNotFoundException

        new_user = User(telegram_id=user_id, username=username, is_admin=False)
        session.add(new_user)
        await session.flush()

        user_class = UserClass(user_id=new_user.id, class_id=class_.id)
        session.add(user_class)

        await message.answer("Вы успешно зарегистрированы!")

    except ClassNotFoundException:
        logger.error(f"Класс {class_number}{class_identifier} не найден!")
        await message.answer(f"Класс {class_number}{class_identifier} не найден!")

    except UserRegisteredException:
        logger.error(f"Пользователь {username} с таким ID уже зарегистрирован")
        await message.answer("Вы уже зарегистрированы")
    