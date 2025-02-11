from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.crud.inventory import get_all_inventory
from app.crud.transaction import get_sent_transactions_by_user_id, get_received_transactions_by_user_id
from app.models.user import User
from app.schemas.info import InfoResponse, CoinHistory

router = APIRouter(prefix="/api/info", tags=["info"])


@router.get("/")
async def get_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    inventory_info = await get_all_inventory(session, current_user.id)
    sent_transactions = await get_sent_transactions_by_user_id(current_user.id, session)
    received_transactions = await get_received_transactions_by_user_id(current_user.id, session)

    return InfoResponse(
        coins=current_user.coins_balance,
        inventory=inventory_info,
        coinHistory=CoinHistory(
            received=received_transactions,
            sent=sent_transactions
        ),
    )
