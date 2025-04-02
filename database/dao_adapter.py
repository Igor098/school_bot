from sqlalchemy.ext.asyncio import AsyncSession

from database.dao import UserDAO, ClassDAO
from database.decorators import with_commit_session


@with_commit_session
async def find_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    user_dao = UserDAO(session)
    user = await user_dao.find_one_or_none_by_telegram_id(telegram_id)
    return user


@with_commit_session
async def find_class(session: AsyncSession, class_number: int, class_identifier: str):
    class_dao = ClassDAO(session)
    class_ = class_dao.find_one_or_none_class(class_number, class_identifier)
