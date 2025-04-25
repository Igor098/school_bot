import json
from pathlib import Path
from typing import Any

import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import null

from database import session
from database.dao import UserDAO, ClassDAO, UserClassDAO, ScheduleDAO
from database.decorators import with_commit_session


@with_commit_session
async def find_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    user_dao = UserDAO(session)
    user = await user_dao.find_one_or_none({"telegram_id": telegram_id})
    return user


@with_commit_session
async def find_class(session: AsyncSession, class_number: int, class_identifier: str | None = None):
    class_dao = ClassDAO(session)
    filters: dict[str, Any] = {"grade": class_number}
    if class_identifier:
        filters["identifier"] = class_identifier

    class_ = await class_dao.find_one_or_none(filters)
    return class_


@with_commit_session
async def add_user(session: AsyncSession, telegram_id: int, username: str, is_admin: bool):
    user_dao = UserDAO(session)
    new_user = dict(telegram_id=telegram_id, username=username, is_admin=is_admin)
    user = await user_dao.add(new_user)
    await session.flush()
    return user


@with_commit_session
async def add_class_for_user(session: AsyncSession, user_id: int, class_id: int):
    user_class_dao = UserClassDAO(session)
    user_class = {
        "user_id": user_id,
        "class_id": class_id
    }
    new_record = await user_class_dao.add(user_class)
    return new_record


@with_commit_session
async def get_user_info(session: AsyncSession, telegram_id: int):
    user_dao = UserDAO(session)
    user_class_dao = UserClassDAO(session)

    user = await user_dao.find_one_or_none({"telegram_id": telegram_id})
    user_info = await user_class_dao.get_user_with_class(user.id)
    return user_info


@with_commit_session
async def get_full_schedule(session: AsyncSession):
    dao = ScheduleDAO(session)
    schedule = await dao.get_full_schedule()
    file_path = Path("schedule.json")
    await save_schedule_to_file(schedule, file_path)


@with_commit_session
async def check_register(session: AsyncSession, telegram_id: int):
    user_dao = UserDAO(session)
    user = await user_dao.find_one_or_none({"telegram_id": telegram_id})
    return True if user else False


async def save_schedule_to_file(schedule: list[dict], file_path: Path):
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(schedule, ensure_ascii=False, indent=4))
