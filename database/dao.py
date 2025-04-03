from typing import Type, Generic, TypeVar, Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from sqlalchemy.orm import Session

from database.models import User, Class, UserClass, Day, Lesson, Subject

from loguru import logger

T = TypeVar("T")  # Означает, что T — это любая модель SQLAlchemy


class BaseDAO(Generic[T]):
    model: Type[T] = None  # Указываем модель в дочерних классах

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def find_one_or_none_by_id(self, data_id: int):
        """Найти запись по ID."""
        try:
            query = select(self.model).filter_by(id=data_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            logger.info(f"Запись {self.model.__name__} с ID {data_id} {'найдена' if record else 'не найдена'}.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    async def find_one_or_none(self, filters: Dict[str, Any]):
        """Найти одну запись по фильтру."""
        logger.info(f"Поиск одной записи {self.model.__name__} по фильтрам: {filters}")
        try:
            query = select(self.model).filter_by(**filters)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            logger.info(f"Запись {'найдена' if record else 'не найдена'} по фильтрам: {filters}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи: {e}")
            raise

    async def find_all(self, filters: Dict[str, Any] = None):
        """Найти все записи по фильтру."""
        filters = filters or {}
        logger.info(f"Поиск всех записей {self.model.__name__} по фильтрам: {filters}")
        try:
            query = select(self.model).filter_by(**filters)
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей: {e}")
            raise

    async def add(self, values: Dict[str, Any]):
        """Добавить одну запись."""
        logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values}")
        try:
            new_instance = self.model(**values)
            self._session.add(new_instance)
            await self._session.flush()
            logger.info(f"Запись {self.model.__name__} успешно добавлена.")
            return new_instance
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise

    async def add_many(self, instances: List[Dict[str, Any]]):
        """Добавить несколько записей."""
        logger.info(f"Добавление {len(instances)} записей {self.model.__name__}")
        try:
            new_instances = [self.model(**values) for values in instances]
            self._session.add_all(new_instances)
            await self._session.flush()
            logger.info(f"Добавлено {len(new_instances)} записей.")
            return new_instances
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise

    async def update(self, filters: Dict[str, Any], values: Dict[str, Any]):
        """Обновить записи по фильтру."""
        logger.info(f"Обновление записей {self.model.__name__} по фильтру: {filters} с параметрами: {values}")
        try:
            query = (
                update(self.model)
                .where(*[getattr(self.model, k) == v for k, v in filters.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            result = await self._session.execute(query)
            await self._session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise

    async def delete(self, filters: Dict[str, Any]):
        """Удалить записи по фильтру."""
        logger.info(f"Удаление записей {self.model.__name__} по фильтру: {filters}")
        if not filters:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")
        try:
            query = delete(self.model).filter_by(**filters)
            result = await self._session.execute(query)
            await self._session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении записей: {e}")
            raise

    async def count(self, filters: Dict[str, Any] = None):
        """Посчитать количество записей по фильтру."""
        filters = filters or {}
        logger.info(f"Подсчет количества записей {self.model.__name__} по фильтру: {filters}")
        try:
            query = select(func.count(self.model.id)).filter_by(**filters)
            result = await self._session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise


class UserDAO(BaseDAO):
    model = User


class ClassDAO(BaseDAO):
    model = Class


class UserClassDAO(BaseDAO):
    model = UserClass

    async def get_user_with_class(self, user_id: int):
        """Возвращает информацию о пользователе и его классе."""
        query = (
            select(User, Class)
            .join(UserClass, User.id == UserClass.user_id)
            .join(Class, UserClass.class_id == Class.id)
            .filter(User.id == user_id)
        )

        result = await self._session.execute(query)
        user, user_class = result.first() if result else (None, None)
        return {"user": user, "class": user_class}


class ScheduleDAO:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_full_schedule(self) -> list[dict]:
        # Пример запроса, который возвращает список записей
        query = (
            select(
                Class.grade,
                Class.identifier,
                Day.name.label("day_name"),
                Lesson.period,
                Subject.name.label("subject_name")
            )
            .join(Lesson, Lesson.class_id == Class.id)
            .join(Day, Lesson.day_id == Day.id)
            .join(Subject, Lesson.subject_id == Subject.id)
            .order_by(Class.grade, Class.identifier, Day.id, Lesson.period)
        )
        result = await self._session.execute(query)
        records = result.mappings().all()

        schedule_by_class = {}
        for row in records:
            # Формируем уникальный ключ для класса, например, "8А"
            class_key = f"{row.get('grade')}{row.get('identifier')}"
            if class_key not in schedule_by_class:
                schedule_by_class[class_key] = {
                    "class_number": row.get("grade"),
                    "class_identifier": row.get("identifier", None),
                    "понедельник": {},
                    "вторник": {},
                    "среда": {},
                    "четверг": {},
                    "пятница": {}
                }
            day = row.get("day_name").lower()  # ожидаем, что в БД названия дней на русском
            period = str(row.get("period"))
            subject = row["subject_name"]
            # Записываем урок в нужный день
            if day in schedule_by_class[class_key]:
                schedule_by_class[class_key][day][period] = subject

        # Получаем список расписаний
        return list(schedule_by_class.values())
