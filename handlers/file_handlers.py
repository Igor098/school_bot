from pathlib import Path
import json
from typing import List

from aiogram import F, types, Router
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.filters import Command
from loguru import logger

from database.dao import ClassDAO
from database.dao_adapter import find_class
from helpers.check_helpers import check_class

file_router = Router()


@file_router.message(F.document & (F.document.file_name.endswith('.json')))
async def import_schedule_file(message: Message):
    # 1. Скачиваем файл к себе
    dest = Path("uploaded_schedule.json")
    await message.bot.download(message.document, destination=dest)



    # 2. Читаем структуру из JSON
    try:
        with dest.open("r", encoding="utf-8") as f:
            schedule_data = json.load(f)
            logger.info(f"loaded data >>> {schedule_data}")

            writeable_data = dict()

            for _class in schedule_data:
                class_is_valid: bool = await check_class(message, _class.get('class_number'), class_identifier=_class.get('class_identifier', ''))
                schedule: dict = _class.get('schedule', [])
                logger.info(f"found schedule >>> {schedule}")
                days: List[str] = list(schedule.keys())

                for day in days:
                    await message.answer(day)

    except (json.JSONDecodeError, FileNotFoundError) as e:
        await message.reply(f"Не удалось прочитать JSON: {e}")
        return
