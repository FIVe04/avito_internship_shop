from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.crud.auth import get_user_by_username
from app.crud.transaction import add_transaction
from app.models.user import User

router = APIRouter(prefix="/api/sendCoin", tags=["transaction"])



@router.post("/")
async def send_coins(
        toUser: str,
        amount: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if toUser == current_user.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send coins to yourself.")

    receiver = await get_user_by_username(toUser, session)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")

    if current_user.coins_balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough coins.")

    current_user.coins_balance -= amount
    receiver.coins_balance += amount

    transaction = await add_transaction(amount, current_user.id, receiver.id, session)

    await session.commit()
    return transaction



