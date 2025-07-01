import sys
import asyncio
from fastapi import FastAPI

from app.api.routes.auth import auth_router


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Blogging App"}


app.include_router(router=auth_router, prefix="/api/v1/auth", tags=["auth"])
