from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.config import settings
from app.core.dependencies import get_db, get_current_user
from app.crud.auth import add_user
from app.models.user import User
from app.services.auth import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()

    if not user:
        print(1)
        password_hash = get_password_hash(form_data.password)
        user = await add_user(form_data.username, password_hash, session)

    elif not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Неавторизован.")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token}


@router.get("/secure")
async def get_secure_data(user: User = Depends(get_current_user)):
    print(settings.INITIAL_COINS)
    return {"username": user.username}



