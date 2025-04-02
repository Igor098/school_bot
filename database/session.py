from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import database_url

engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
