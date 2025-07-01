from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import GeneralConfig


async_engine = create_async_engine(url=GeneralConfig.PGDB_URL, echo=True)


async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    # Yields an AsyncSession instance or None (after completion)
    async with async_session() as session:
        yield session
