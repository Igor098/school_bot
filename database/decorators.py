from functools import wraps
from typing import Callable, Awaitable, TypeVar, Any

from dependencies.dao_dep import get_session_with_commit, get_session_without_commit

T = TypeVar("T", bound=Callable[..., Awaitable[Any]])


def with_commit_session(func: T) -> T:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Используем асинхронный генератор для получения сессии
        async for session in get_session_with_commit():
            kwargs["session"] = session
            result = await func(*args, **kwargs)
            await session.commit()
            return result

    return wrapper


def without_commit_session(func: T) -> T:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Используем асинхронный генератор для получения сессии
        async for session in get_session_without_commit():
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
