from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_db
from app.models.user import User


async def add_user(username: str, hashed_password: str, session: AsyncSession) -> User:
    user = User(username=username,
                hashed_password=hashed_password,
                coins_balance=settings.INITIAL_COINS
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    return user
