from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Class

from loguru import logger


class UserDAO:
    model = User

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user, session: AsyncSession):
        try:
            self._session.add(user)
            logger.info(f"Запись {self.model.__name__} успешно добавлена.")
            await self._session.flush()
            return user

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise

    async def find_one_or_none_by_telegram_id(self, telegram_id: int):
        try:
            query = select(self.model).filter_by(id=telegram_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Запись {self.model.__name__} с Telegram ID {telegram_id} {'найдена' if record else 'не найдена'}."
            logger.info(log_message)
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {telegram_id}: {e}")
            raise


class ClassDAO:
    model = Class

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_one_or_none_class(self, class_number: int, class_identifier: str):
        try:
            query = select(self.model).filter(Class.grade == class_number, Class.identifier == class_identifier)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Запись {self.model.__name__} с классом {class_number}{class_identifier} {'найдена' if record else 'не найдена'}."
            logger.info(log_message)
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {class_number}: {e}")
            raise
