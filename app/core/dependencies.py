from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.models.user import User
from app.services.auth import oauth2_scheme, verify_token


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

        await session.commit()
        await session.close()


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    result = await session.execute(select(User).filter(User.id == int(payload["sub"])))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
