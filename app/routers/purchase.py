from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.crud.auth import get_user_by_id
from app.crud.inventory import add_purchase_to_inventory
from app.crud.product import get_product_by_name
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/api/buy", tags=["purchase"])


@router.post("/")
async def purchase(item: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    product = await get_product_by_name(db, item)
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")

    user = await get_user_by_id(user.id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if user.coins_balance < product.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough coins")

    user.coins_balance -= product.price

    inventory = await add_purchase_to_inventory(db, product.id, user.id)

    await db.commit()

    return inventory




