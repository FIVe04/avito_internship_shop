from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import Inventory


async def add_purchase_to_inventory(db: AsyncSession, product_id: int, user_id: int) -> Inventory:
    result = await db.execute(select(Inventory).filter(Inventory.user_id == user_id, Inventory.product_id == product_id))
    inventory_item = result.scalar_one_or_none()
    if inventory_item:
        inventory_item.quantity += 1
    else:
        inventory_item = Inventory(user_id=user_id, product_id=product_id, quantity=1)
        db.add(inventory_item)

    await db.commit()
    await db.refresh(inventory_item)
    return inventory_item