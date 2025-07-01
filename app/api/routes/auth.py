from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin
from app.db.session import get_db_session
from app.db.repositories.user import get_user_by_username, get_user_by_email, create_new_user
from app.services.security import password_matches

auth_router = APIRouter()


@auth_router.post("/sign-up")
async def user_sign_up(user: UserCreate, async_session: Annotated[AsyncSession, Depends(get_db_session)]):
    if await get_user_by_username(async_session, user.username) or await get_user_by_email(async_session, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return {"Created User ID": await create_new_user(async_session, user)}


@auth_router.post("/login")
async def user_login(user: UserLogin, async_session: Annotated[AsyncSession, Depends(get_db_session)]):
    db_user = await get_user_by_username(async_session, user.username)
    if not db_user or not password_matches(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials provided",
        )
    return {"message": f"Hello {db_user.username}"}
