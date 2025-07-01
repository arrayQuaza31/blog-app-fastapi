from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.security import hash_password


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    result = await db_session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    result = await db_session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_new_user(db_session: AsyncSession, user: UserCreate) -> str | None:
    new_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hash_password(password=user.password),
    )
    db_session.add(new_user)
    await db_session.commit()
    return new_user.id
