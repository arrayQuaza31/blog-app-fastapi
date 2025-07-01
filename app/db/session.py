from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import Config


async_engine = create_async_engine(url=Config.PGDB_URL, echo=True)


async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
