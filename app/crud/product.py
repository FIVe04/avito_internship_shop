from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.product import Product
from app.shared.products_sample import products_to_add


async def add_products_to_db(db: AsyncSession):
    for product in products_to_add:
        query = select(Product).filter(Product.name == product["name"])
        result = await db.execute(query)
        existing_product = result.scalars().first()

        if not existing_product:
            new_product = Product(name=product["name"], price=product["price"])
            db.add(new_product)
    await db.commit()


async def get_product_by_name(db: AsyncSession, name: str) -> Product:
    result = await db.execute(select(Product).filter(Product.name == name))
    product = result.scalar_one_or_none()
    return product


async def get_product_by_id(db: AsyncSession, id: int) -> Product:
    result = await db.execute(select(Product).filter(Product.id == id))
    product = result.scalar_one_or_none()
    return product
