import sys
import asyncio
from sqlalchemy import text

from app.db.session import async_engine


async def test_connection():
    async with async_engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(f"DB CONNECTED: {result.scalar_one()}")


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_connection())
