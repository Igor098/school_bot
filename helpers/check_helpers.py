from typing import List

from aiogram.types import Message

from database.dao_adapter import find_class
from loguru import logger


async def check_class(message: Message, class_number: int, class_identifier: str | None) -> bool:
    is_found = await find_class(class_number=class_number, class_identifier=class_identifier)
    if is_found:
        await message.answer(f"Найден класс: {class_number}{class_identifier if class_identifier else ''}")
        logger.info(f"Найден класс: {class_number}{class_identifier if class_identifier else ''}")
        return True
    else:
        await message.answer(f"Класс {class_number}{class_identifier if class_identifier else ''} не найден!")
        logger.error(f"Класс {class_number}{class_identifier if class_identifier else ''} не найден!")
        return False


async def check_days(message: Message, days: List[str]) -> bool:
    pass